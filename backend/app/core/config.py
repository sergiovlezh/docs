from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_ROOT / ".env", _ROOT / ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    DATABASE_URL: str
    SECRET_KEY: str

    DEBUG: bool = False
    TOKEN_EXPIRE_HOURS: int = 12
    MIN_PASSWORD_LENGTH: int = 8


settings = Settings()
