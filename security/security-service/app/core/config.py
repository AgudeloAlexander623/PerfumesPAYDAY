from datetime import datetime
from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configuración de persistencia compartida por la app y Alembic."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Base de datos propia del servicio; el valor por defecto solo sirve en local.
    database_url: str = Field(
        default="postgresql+asyncpg://security:security@localhost:5432/security_db"
    )

    # Ciclo de vida de la sesión definido en ADR-0009.
    refresh_ttl_days: int = Field(default=7, ge=1, le=30)
    session_absolute_ttl_days: int = Field(default=30, ge=1, le=365)

    # Umbrales de bloqueo temporal confirmados para la beta.
    login_max_failed_attempts: int = Field(default=5, ge=1, le=20)
    login_lockout_minutes: int = Field(default=15, ge=1, le=1440)

    @field_validator("database_url")
    @classmethod
    def database_url_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("DATABASE_URL no puede estar vacía.")
        return value

    @model_validator(mode="after")
    def session_ttls_are_consistent(self) -> Self:
        """Evita que la sesión absoluta sea menor que la inactividad."""
        if self.session_absolute_ttl_days < self.refresh_ttl_days:
            raise ValueError(
                "SESSION_ABSOLUTE_TTL_DAYS debe ser mayor o igual que REFRESH_TTL_DAYS."
            )
        return self


class Settings(DatabaseSettings):
    """Variables de entorno completas del servicio de seguridad.

    Los nombres de los campos se leen en mayúsculas y sin distinguir
    mayúsculas de minúsculas: `jwt_private_key` ← `JWT_PRIVATE_KEY`.
    """

    environment: Literal["development", "test", "production"] = "development"
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)

    jwt_issuer: str = "perfumesgold-security"
    jwt_audience: str = "perfumesgold-api"
    jwt_private_key: str
    jwt_public_key: str | None = None
    jwt_key_id: str | None = None
    jwt_access_ttl_seconds: int = Field(default=900, ge=60, le=3600)

    # Rotación: la clave anterior sigue publicada durante el solape (ADR-0003).
    # jwt_previous_key_rotated_at se expresa en ISO 8601; si falta se toma el arranque.
    jwt_previous_private_key: str | None = None
    jwt_previous_public_key: str | None = None
    jwt_previous_key_id: str | None = None
    jwt_previous_key_rotated_at: datetime | None = None
    jwt_key_overlap_seconds: int = Field(default=86400, ge=60, le=604800)

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
def get_database_settings() -> DatabaseSettings:
    """Carga únicamente la configuración de base de datos que necesita Alembic."""
    return DatabaseSettings()  # type: ignore[call-arg]


@lru_cache
def get_settings() -> Settings:
    """Carga la configuración completa una sola vez por proceso."""
    return Settings()  # type: ignore[call-arg]
