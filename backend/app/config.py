from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./tracker.db"
    cors_origins: str = "http://localhost:3000"
    admin_api_key: str = "change-me-in-production"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
@lru_cache
def get_settings() -> Settings: return Settings()
