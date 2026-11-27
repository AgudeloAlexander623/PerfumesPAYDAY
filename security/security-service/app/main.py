from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.errors import register_error_handlers
from app.api.routes import health, jwks
from app.core.config import Settings, get_settings
from app.core.security import JwtIssuer
from app.db import create_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Inicializa el pool de base de datos y lo libera al apagar el servicio."""
    database = create_database(app.state.settings.database_url)
    app.state.database = database
    try:
        yield
    finally:
        await database.engine.dispose()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construye la aplicación; `uvicorn` la invoca con `--factory`."""
    resolved_settings = settings or get_settings()
    issuer = JwtIssuer.from_settings(resolved_settings)

    app = FastAPI(
        title="Perfumes GOLD Security Service",
        version="0.1.0",
        description="Emisión de tokens JWT RS256 y publicación de JWKS.",
        docs_url=None if resolved_settings.is_production else "/docs",
        redoc_url=None,
        openapi_url=None if resolved_settings.is_production else "/openapi.json",
        lifespan=lifespan,
    )

    app.state.settings = resolved_settings
    app.state.jwt_issuer = issuer

    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(jwks.router)

    return app