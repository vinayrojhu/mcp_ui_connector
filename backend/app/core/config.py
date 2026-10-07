from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///./adaptive_ui.db"
    jwt_secret: str = "development-only-change-this-secret"
    encryption_key: str = ""
    llm_provider: str = "mock"
    llm_api_endpoint: str = ""
    llm_model: str = "mock"
    llm_api_key: str = ""
    llm_timeout: int = 30
    max_connector_steps: int = 30
    max_execution_seconds: int = 300
    approval_expiration_seconds: int = 300
    allowed_domains: str = "localhost,127.0.0.1"
    allowed_applications: str = "mock-fund-portal"
    worker_auth_secret: str = "development-worker-secret"
    artifact_dir: str = "./artifacts"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
