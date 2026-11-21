# Bitácora del backend

## 2026-11-20 — Persistencia de `security-service` y documentación actualizada

### Resumen del día

Se completó la fase de base de datos del servicio de seguridad. `security-service` ya dispone de configuración de persistencia, modelos `User` y `UserSession`, migración Alembic y ciclo de vida del pool en FastAPI. Docker Compose incorporó PostgreSQL 16 para `security_db`, healthcheck, volumen propio y dependencia desde `security`. Los servicios Node dejaron de requerir `JWT_PUBLIC_KEY` en contenedores y ahora validan tokens contra el JWKS del servicio de seguridad.

También se revisó el README raíz y la documentación global para reflejar el estado real del backend y de `security_db`, y se actualizó esta bitácora.

### Cambios en `security-service`

- `pyproject.toml`: agregadas `SQLAlchemy[asyncio]`, `asyncpg` y `alembic`. El extra `asyncio` instala `greenlet`, necesario para el ORM asíncrono.
- `app/core/config.py`: separada `DatabaseSettings` de `Settings`, para que Alembic pueda migrar sin exigir `JWT_PRIVATE_KEY`. Nuevas variables:
  - `DATABASE_URL`
  - `REFRESH_TTL_DAYS=7`
  - `SESSION_ABSOLUTE_TTL_DAYS=30`
  - `LOGIN_MAX_FAILED_ATTEMPTS=5`
  - `LOGIN_LOCKOUT_MINUTES=15`
  - Validación para impedir que la sesión absoluta sea menor que la de inactividad.
- `app/db/`: base declarativa con convención de nombres, `TimestampMixin`, modelos `users` y `sessions`, y fábrica asíncrona de sesiones.
- `app/domain/users.py`: enums `UserRole` y `UserStatus`.
- `app/main.py`: el lifespan crea el pool al arrancar y llama a `dispose()` al apagar.
- `alembic.ini` y `migrations/`: configuración, plantilla y revisión `0001_create_identity_tables.py`. La migración crea la extensión `citext`, ambas tablas, checks, índices y claves foráneas; `downgrade` revierte todo.
- `Dockerfile`: copia `alembic.ini` y `migrations/` dentro de la imagen.
- Pruebas: ampliados `tests/test_config.py` y creado `tests/test_models.py`.

### Cambios en infraestructura y configuración

- `Backend/docker-compose.yml`:
  - Servicio `security-db` con PostgreSQL 16, volumen `security-db-data` y healthcheck.
  - `security` depende de la salud de `security-db`.
  - Configuración de BD, TTLs y umbrales de bloqueo inyectada al contenedor.
  - `x-environment` usa `JWT_JWKS_URL` en lugar de `JWT_PUBLIC_KEY` para `gateway`, `catalog` y `orders`.
- `Backend/.env.example`: documentados `JWT_JWKS_URL`, `JWT_PRIVATE_KEY` como requisito de Compose y `SECURITY_DB_PASSWORD`.
- `security/security-service/.env.example`: documentadas BD, TTLs y umbrales de login.

### Cambios en documentación

- `README.md`: estado real del backend y del servicio de seguridad, estructura con `alembic.ini`/`migrations/`, stack Python actualizado, modelo operativo de `users`/`sessions`, instrucciones de migraciones, arranque con Docker Compose, enlace a la bitácora y checklist corregido.
- `docs/README.md`, `docs/architecture.md`, `docs/PLAN.md` y `docs/ROADMAP.md`: actualizado el estado de `security_db` y el próximo paso.
- `docs/adr/0003-jwt-rs256.md`: JWKS en Docker Compose marcado como implementado.
- `docs/adr/0009-sesiones-refresh-cookies.md` y `docs/adr/0011-politica-contrasenas.md`: pendientes y umbral de bloqueo ajustados a lo implementado.
- `docs/adr/0002-fastify-workspaces.md` y `docs/adr/0004-propiedad-datos.md`: enlaces a la bitácora corregidos.
- `security/docs/README.md`: estado, tecnologías, comandos y referencias del servicio actualizados.

### Pruebas ejecutadas

```text
pytest: 24 passed, 1 warning de dependencia (Starlette/httpx)
python3 -m compileall -q app migrations tests: OK
docker compose -f Backend/docker-compose.yml config --quiet: OK
alembic upgrade head --sql sin JWT_PRIVATE_KEY: OK
PostgreSQL 16 real: upgrade y downgrade OK
```

En PostgreSQL se verificaron `users`, `sessions`, `alembic_version` y las restricciones `ck_users_role`, `ck_users_status`, `uq_users_email`, `uq_sessions_refresh_token_hash` y las claves foráneas. El contenedor temporal fue eliminado.

### Incidencias encontradas y corregidas

1. SQLAlchemy asíncrono fallaba sin `greenlet`; corregido con `SQLAlchemy[asyncio]`.
2. Alembic no podía leer la configuración sin la clave JWT; corregido separando `DatabaseSettings`.
3. Los nombres de los `CHECK` quedaban duplicados por la convención de Alembic (`ck_users_ck_users_role`); corregido usando nombres cortos en modelo y migración.
4. La migración fallaba en PostgreSQL real porque no existía el tipo `citext`; corregido con `CREATE EXTENSION IF NOT EXISTS citext`.

### Pendiente

- Argon2id y validador compartido de contraseñas, incluida la lista local de valores comunes.
- Repositorios y endpoints de registro, login, refresh y logout.
- Cookies `__Host-ppd_refresh`, CSRF y `Cache-Control: no-store`.
- Hardening JWT en Node: validación de `typ`, `jti`, `WWW-Authenticate` y `503` si el JWKS no responde.
- Contrato `docs/api/security.openapi.yaml`.

---

## 2026-11-13 — Capa JWT del backend

**Fecha:** 2026-11-13

### Resumen del día

Durante el día se completó la capa de autenticación JWT del backend. En Node.js se creó el módulo compartido de validación RS256 con claims (sub, iss, aud, exp, iat, jti y roles), guards de autenticación y rol, y configuración por entorno con fallo cerrado. El gateway quedó operativo con proxy /api/v1, CORS con orígenes explícitos y rechazo del comodín, rate limit global y estricto para auth, timeout, respuestas 503 con envelope, propagación de x-request-id y limpieza de cabeceras internas. Se añadieron 47 pruebas y la cobertura quedó en 73,09 %. En Python/FastAPI se construyó security-service: carga de clave RSA, firma RS256, JWKS, /health, envelope de errores, Dockerfile y servicio en Docker Compose. Se añadieron 20 pruebas. La integración extremo a extremo quedó verificada: el emisor generó un token, el gateway lo validó por JWKS y lo proxificó; sin token respondió 401. También se actualizó la bitácora y se realizaron cambios en el rol de PO (Product Owner) del proyecto.

### Cambios en el rol de PO

- Se realizaron cambios en el rol de PO (Product Owner) del proyecto.
