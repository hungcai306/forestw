from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Hue ForestWatch API"
    environment: str = "production"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/forestwatch"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 480
    cors_origins: str = "http://localhost:5173"
    sadmin_email: str = "sadmin@example.gov.vn"
    sadmin_password: str = "ChangeMe123!"
    admin_api_base: str = "https://34tinhthanh.com/api"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
