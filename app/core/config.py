from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )

    env: str = Field(default="dev")
    secret_key: str = Field(default="dev-secret-key")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    database_url: str = Field(default="sqlite:///./app.db")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
