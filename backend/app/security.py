import base64
import hashlib
import hmac
import json
import secrets
import time

from app.config import get_settings


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240_000)
    return f"pbkdf2_sha256$240000${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_value, digest_value = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_value.encode())
        expected = base64.urlsafe_b64decode(digest_value.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str, roles: list[str]) -> tuple[str, int]:
    settings = get_settings()
    expires_in = settings.access_token_expire_minutes * 60
    payload = {"sub": subject, "roles": roles, "exp": int(time.time()) + expires_in}
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    signature = hmac.new(settings.secret_key.encode(), encoded_payload.encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{encoded_payload}.{encoded_signature}", expires_in


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    encoded_payload, encoded_signature = token.split(".", 1)
    expected = hmac.new(settings.secret_key.encode(), encoded_payload.encode(), hashlib.sha256).digest()
    supplied = base64.urlsafe_b64decode(encoded_signature + "=")
    if not hmac.compare_digest(expected, supplied):
        raise ValueError("Invalid token signature")
    payload = json.loads(base64.urlsafe_b64decode(encoded_payload + "==").decode())
    if int(payload["exp"]) <= int(time.time()):
        raise ValueError("Token expired")
    return payload
