from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables de entorno del servicio.

    Los nombres de los campos se leen en mayúsculas y sin distinguir
    mayúsculas de minúsculas: `jwt_private_key` ← `JWT_PRIVATE_KEY`.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    environment: Literal["development", "test", "production"] = "development"
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)

    jwt_issuer: str = "perfumespayday-security"
    jwt_audience: str = "perfumespayday-api"
    jwt_private_key: str
    jwt_public_key: str | None = None
    jwt_key_id: str | None = None
    jwt_access_ttl_seconds: int = Field(default=900, ge=60, le=3600)

    @field_validator("jwt_private_key")
    @classmethod
    def private_key_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("JWT_PRIVATE_KEY no puede estar vacía.")
        return value

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Carga la configuración una sola vez por proceso."""
    return Settings()  # type: ignore[call-arg]