from collections.abc import AsyncIterator
from dataclasses import dataclass

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@dataclass(frozen=True)
class Database:
    """Agrupa el pool y la fábrica para evitar estados globales."""

    engine: AsyncEngine
    sessions: async_sessionmaker[AsyncSession]


def create_database(url: str) -> Database:
    """Crea el pool sin abrir conexiones; Alembic gestiona el esquema."""
    engine = create_async_engine(url, pool_pre_ping=True)
    return Database(
        engine=engine,
        sessions=async_sessionmaker(engine, expire_on_commit=False),
    )


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """Entrega una sesión por petición y siempre la cierra."""
    database: Database = request.app.state.database
    async with database.sessions() as session:
        yield session
