from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):
    app_name: str = "SentinelAI API"
    environment: str = "local"
    database_url: str = "sqlite:///./sentinelai.db"
    secret_key: str = "local-development-secret-change-me"
    access_token_expire_minutes: int = 60
    demo_admin_email: str = "admin@sentinelai.example"
    demo_admin_password: str = "change-me"
    neo4j_uri: str = ""
    neo4j_user: str = "neo4j"
    neo4j_password: str = "change-me"
    demo_mode: bool = True
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60
    max_request_bytes: int = 1_000_000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_runtime(self) -> "Settings":
        if self.environment == "production" and (self.secret_key == "local-development-secret-change-me" or self.demo_mode):
            raise ValueError("Production requires a non-default secret key and demo_mode=false")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
