from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "CRE Investment AI Platform"
    database_url: str = "postgresql+psycopg://cre_ai:cre_ai_password@db:5432/cre_ai"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    collection_interval_minutes: int = 30
    min_price_rub: int = 100_000_000
    max_price_rub: int = 400_000_000
    min_building_year: int = 2016
    allowed_floor: int = 1
    allowed_property_types: str = "street_retail,retail,free_use,federal_tenant"

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    @property
    def property_types(self) -> set[str]:
        return {item.strip() for item in self.allowed_property_types.split(",") if item.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

