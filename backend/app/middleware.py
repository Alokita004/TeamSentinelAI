import time
import logging
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from uuid import uuid4

from app.config import get_settings


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allowed(self, key: str) -> bool:
        settings = get_settings()
        now = time.monotonic()
        hits = self._hits[key]
        while hits and now - hits[0] >= settings.rate_limit_window_seconds:
            hits.popleft()
        if len(hits) >= settings.rate_limit_requests:
            return False
        hits.append(now)
        return True


rate_limiter = InMemoryRateLimiter()
logger = logging.getLogger("sentinelai.api")


async def security_middleware(request: Request, call_next):
    settings = get_settings()
    request_id = request.headers.get("X-Request-ID", "")[:100] or str(uuid4())
    request.state.request_id = request_id
    content_length = request.headers.get("content-length")
    try:
        request_size = int(content_length) if content_length else 0
    except ValueError:
        request_size = settings.max_request_bytes + 1
    if request_size > settings.max_request_bytes:
        return JSONResponse(status_code=413, content={"code": "PAYLOAD_TOO_LARGE", "message": "Request body exceeds the configured limit", "request_id": request_id})
    if not rate_limiter.allowed(request.client.host if request.client else "unknown"):
        return JSONResponse(status_code=429, content={"code": "RATE_LIMITED", "message": "Too many requests", "request_id": request_id}, headers={"Retry-After": str(settings.rate_limit_window_seconds)})
    started = time.perf_counter()
    response = await call_next(request)
    logger.info("request_complete", extra={"request_id": request_id, "method": request.method, "path": request.url.path, "status_code": response.status_code, "duration_ms": round((time.perf_counter() - started) * 1000, 2)})
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response
