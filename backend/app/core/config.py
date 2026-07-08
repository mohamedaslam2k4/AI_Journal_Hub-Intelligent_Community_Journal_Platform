from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Journal Hub"
    environment: str = "development"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    mongodb_uri: str
    mongodb_db: str = "ai_journal_hub"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    embedding_model: str = "text-embedding-004"
    vector_index_name: str = "journal_embedding_index"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
