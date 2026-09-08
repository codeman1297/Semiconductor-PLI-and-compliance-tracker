"""Application settings, loaded from environment / .env."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    """Every configurable value in one place. See .env.example."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "India Semiconductor Incentive Compliance Tracker"
    database_url: str = f"sqlite:///{DATA_DIR / 'tracker.db'}"
    base_url: str = "http://127.0.0.1:8000"
    secret_key: str = "dev-only-insecure-key"
    admin_email: str = "admin@example.com"
    llm_answers_enabled: bool = False
    anthropic_api_key: str = ""
    cookie_secure: bool = False
    debug: bool = False

    disclaimer: str = (
        "Informational only. Not legal, financial, or tax advice. "
        "Verify against the current official notification before acting."
    )


@lru_cache
def get_settings() -> Settings:
    """Cached accessor so settings are parsed once per process."""
    return Settings()
