# Security Service

Servicio de identidad de **Perfumes GOLD**. Emite access tokens RS256, publica su JWKS y es dueño exclusivo de `security_db`.

## Estado actual (2026-11-20)

- Emisor JWT RS256 con `sub`, `iss`, `aud`, `iat`, `exp`, `jti`, `roles` y `typ: "access"`.
- JWKS público en `/.well-known/jwks.json`; Docker Compose lo consume mediante `JWT_JWKS_URL`.
- Modelo persistente de `users` y `sessions` con SQLAlchemy asíncrono.
- Migración versionada `0001_create_identity_tables.py` ejecutable con Alembic.
- **Aún no hay** endpoints de registro, login, refresh, logout, perfil ni cambio de contraseña.

## Tecnologías

- Python 3.12 y FastAPI.
- Pydantic Settings para configuración por entorno.
- PyJWT para firma RS256 y publicación de claves.
- SQLAlchemy 2 con `asyncio`, `asyncpg` y PostgreSQL 16.
- Alembic para migraciones.
- pytest para pruebas.
- Argon2id: decisión aceptada en [ADR-0011](../../docs/adr/0011-politica-contrasenas.md), pendiente de instalar.

## Ejecución local

```bash
cd security/security-service
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
cp .env.example .env
# Ajusta DATABASE_URL y JWT_PRIVATE_KEY en .env
.venv/bin/alembic upgrade head
.venv/bin/python -m pytest
```

En Docker Compose, el servicio `security` espera a que `security-db` esté sano. La ejecución de migraciones dentro del contenedor es:

```bash
docker compose -f Backend/docker-compose.yml exec security alembic upgrade head
```

## Referencias

- [ADR-0003 — JWT RS256 y JWKS](../../docs/adr/0003-jwt-rs256.md)
- [ADR-0009 — Sesiones, refresh tokens y cookies](../../docs/adr/0009-sesiones-refresh-cookies.md)
- [ADR-0011 — Política de contraseñas](../../docs/adr/0011-politica-contrasenas.md)
- [Bitácora del backend](../../Backend/docs/Bitacora.alex.md)
