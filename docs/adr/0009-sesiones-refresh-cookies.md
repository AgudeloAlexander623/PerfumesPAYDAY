# ADR-0009 — Sesiones, refresh tokens y cookies

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-14 |
| Decisores | Equipo, responsable de seguridad |
| Relacionados | CU-01 a CU-04, CU-24, [ADR-0003](0003-jwt-rs256.md), [ADR-0010](0010-revocacion-access-tokens.md), [ADR-0011](0011-politica-contrasenas.md), [`security.md`](../security.md) |

## Contexto

Los casos de uso CU-01 a CU-04 definen registro, inicio de sesión, renovación y cierre de sesión. El backend ya emite y valida access tokens JWT RS256, pero todavía no existe el ciclo de vida de la sesión: no hay refresh tokens, cookies, rotación ni revocación.

Hace falta una decisión explícita porque afecta el contrato público, la base `security_db`, el frontend, el gateway y las pruebas de seguridad.

## Decisión

Se separa la **autenticación stateless** (access token JWT) de la **sesión revocable** (refresh token opaco persistido en `security_db`).

### 1. Access token

- JWT firmado con RS256 por `security-service`.
- Vida útil: **15 minutos** (`JWT_ACCESS_TTL_SECONDS=900`, configurable entre 60 y 3600).
- Claims obligatorios: `sub`, `iss`, `aud`, `iat`, `exp`, `jti`, `roles` y `typ: "access"`.
- `sub` es el UUID del usuario; `roles` contiene al menos un rol (`customer` o `admin`).
- `jti` es obligatorio y único; se usa para trazabilidad y auditoría, no como denylist en la beta.
- El access token se devuelve en el cuerpo de la respuesta y el frontend lo mantiene **en memoria**. No se guarda en `localStorage` ni en una cookie accesible por JavaScript.
- El access token no contiene refresh token, contraseña ni datos personales innecesarios.

### 2. Refresh token

- **No es un JWT.** Es un valor opaco de 32 bytes aleatorios generados con un CSPRNG y codificados en base64url (43 caracteres).
- Se guarda en `security_db` **solo como hash SHA-256** en `sessions.refresh_token_hash`, con índice único.
- Nunca se devuelve en el cuerpo, en la URL ni en logs; solo viaja en la cookie.
- La rotación es obligatoria en cada refresh: el token usado se revoca y se emite uno nuevo.
- La reutilización de un token ya rotado o revocado revoca **todas las sesiones del usuario** y responde `401`.

La razón para usar un token opaco es que se puede revocar de inmediato, no depende de la clave de firma y evita que un refresh token JWT se confunda con un access token.

### 3. Cookie

| Atributo | Producción | Desarrollo |
|---|---|---|
| Nombre | `__Host-ppd_refresh` | `ppd_refresh` |
| `HttpOnly` | `true` | `true` |
| `Secure` | `true` | `false` |
| `SameSite` | `Lax` | `Lax` |
| `Path` | `/` | `/api/v1/auth` |
| `Domain` | No se define | No se define |
| `Max-Age` | 7 días | 7 días |

Reglas:

- El prefijo `__Host-` exige `Secure`, `Path=/` y ausencia de `Domain`; se usa solo en producción con HTTPS.
- En desarrollo se usa `ppd_refresh` con `Path=/api/v1/auth` y sin `Secure` para trabajar sobre HTTP local.
- Si el frontend y la API se despliegan en sitios distintos, se cambia a `SameSite=None` con `Secure=true` y se registra la decisión. Para la beta se asume despliegue **same-site**.
- La cookie se elimina con los mismos atributos con los que se creó.
- Las respuestas de login, refresh y logout llevan `Cache-Control: no-store`.

### 4. Vida de la sesión

| Parámetro | Valor | Configuración |
|---|---|---|
| Access token | 15 minutos | `JWT_ACCESS_TTL_SECONDS` |
| Refresh por inactividad | 7 días | `REFRESH_TTL_DAYS` |
| Vida absoluta de la sesión | 30 días | `SESSION_ABSOLUTE_TTL_DAYS` |
| Ventana de rotación | En cada refresh | — |

- Cada refresh extiende la expiración por inactividad, pero **nunca** supera la vida absoluta.
- `expires_at = min(now + REFRESH_TTL, absolute_expires_at)`.
- Una sesión expirada o revocada no se reutiliza.
- Se permite más de una sesión activa por usuario: una por dispositivo.
- Un job periódico elimina sesiones expiradas y sus hashes.

### 5. Modelo de datos

`security_db` es propiedad de `security-service`. No se comparte con `catalog` ni `orders`; ADR-0004 aplica a esas bases, no a esta.

```text
users
  id                uuid primary key
  name              varchar(120) not null
  email             citext unique not null
  password_hash     text not null
  role              varchar(20) not null check (role in ('customer', 'admin'))
  status            varchar(20) not null default 'active' check (status in ('active', 'disabled'))
  created_at        timestamptz not null default now()
  updated_at        timestamptz not null default now()
  last_login_at     timestamptz null

sessions
  id                  uuid primary key
  user_id             uuid not null references users(id) on delete cascade
  family_id           uuid not null
  refresh_token_hash  char(64) unique not null
  expires_at          timestamptz not null
  absolute_expires_at timestamptz not null
  revoked_at          timestamptz null
  replaced_by         uuid null references sessions(id)
  user_agent          varchar(255) null
  ip                  inet null
  created_at          timestamptz not null default now()
  last_used_at        timestamptz null
```

- `family_id` agrupa la cadena de rotaciones de un mismo dispositivo.
- `replaced_by` permite reconstruir la cadena y detectar reutilización.
- Los índices cubren `user_id`, `family_id`, `expires_at` y `refresh_token_hash`.

### 6. Flujos

#### Registro

1. Validar nombre, correo y contraseña en el servidor.
2. Normalizar el correo a minúsculas y verificar unicidad.
3. Hashear la contraseña según ADR-0011.
4. Crear el usuario con rol `customer` y estado `active`.
5. Responder `201` con los datos públicos del usuario.
6. No iniciar sesión automáticamente.

#### Login

1. Buscar al usuario por correo normalizado.
2. Verificar la contraseña con comparación de tiempo constante.
3. Responder `401` genérico si el correo no existe o la contraseña no coincide.
4. Responder `403` si el usuario está deshabilitado.
5. Crear la sesión, generar el refresh token y guardar su hash.
6. Emitir el access token y devolverlo en el cuerpo junto con los datos mínimos del usuario.
7. Enviar el refresh token en la cookie.
8. Actualizar `last_login_at` y reiniciar el contador de intentos fallidos.

#### Refresh

1. Leer el refresh token de la cookie; nunca del cuerpo ni de la URL.
2. Buscar la sesión por el hash SHA-256.
3. Validar que no esté revocada, que no haya expirado y que el usuario esté activo.
4. Bloquear la fila y rotar de forma atómica: revocar la sesión actual y crear la nueva con el mismo `family_id`.
5. Marcar `replaced_by` en la sesión anterior.
6. Emitir un nuevo access token y una nueva cookie.
7. Si el token ya estaba revocado o reemplazado, revocar todas las sesiones del usuario y responder `401`.

#### Logout

1. Leer el refresh token de la cookie.
2. Revocar la sesión correspondiente.
3. Eliminar la cookie.
4. Responder `204` aunque no exista una sesión activa.
5. `logout?all=true` revoca todas las sesiones del usuario y requiere un access token válido.

#### Cambio de contraseña

1. Exigir la contraseña actual.
2. Validar la nueva según ADR-0011.
3. Actualizar el hash.
4. Revocar todas las sesiones del usuario, incluida la actual.
5. Responder `204` y exigir un nuevo login.

### 7. CSRF

- La cookie usa `SameSite=Lax` y el gateway valida `Origin`/`Referer` contra `CORS_ORIGINS` en `POST /api/v1/auth/refresh` y `POST /api/v1/auth/logout`.
- En producción, si falta `Origin` y `Referer` en una operación con cookie, se responde `403`.
- En desarrollo se permite la ausencia de `Origin` para facilitar pruebas con `curl`, pero se registra una advertencia.
- Para la beta no se implementa double-submit token; si el despliegue queda cross-site, se reevalúa.
- El gateway reenvía la cookie al servicio interno y no acepta refresh token en el cuerpo.

### 8. Contrato y prefijo

- Las rutas públicas son `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh` y `POST /api/v1/auth/logout`.
- El gateway conserva el prefijo `/api/v1`; `security-service` monta exactamente esas rutas.
- `GET /api/v1/users/me`, `PATCH /api/v1/users/me` y `PATCH /api/v1/users/me/password` requieren access token.
- El contrato detallado se escribe en `docs/api/security.openapi.yaml` en la Fase 1.

### 9. Persistencia y stack

- PostgreSQL 16 en el servicio `security` de Docker Compose, con volumen propio y healthcheck.
- SQLAlchemy 2.x async + `asyncpg` para el acceso a datos.
- Alembic para migraciones versionadas.
- Repositorios y servicios separados de los routers; sin SQL en los endpoints.
- Sin joins entre bases; `security-service` no consulta `catalog_db` ni `orders_db`.

## Alternativas consideradas

| Tema | Alternativa | Veredicto |
|---|---|---|
| Refresh token | JWT firmado con `typ=refresh` | Rechazado: no se revoca de inmediato y puede confundirse con un access token |
| Refresh token | Guardar el valor completo en BD | Rechazado: una fuga de BD permitiría reutilizarlo |
| Cookie | `localStorage` para refresh | Rechazado: accesible por XSS |
| Cookie | `SameSite=Strict` | Rechazado: rompe flujos de navegación normales; `Lax` es suficiente para la beta |
| Rotación | Sin rotación, solo expiración | Rechazado: no detecta robo ni reutilización |
| Sesión | Una sola sesión por usuario | Rechazado: CU-02 permite una por dispositivo |

## Consecuencias

- `security-service` necesita base de datos, migraciones, hashing y endpoints reales.
- El frontend debe implementar refresh silencioso con una sola petición en vuelo (single-flight).
- El gateway debe reenviar cookies y validar el origen en refresh/logout.
- Las pruebas deben cubrir rotación, reutilización, expiración, logout idempotente y cambio de contraseña.
- La sesión es revocable, pero el access token sigue siendo válido hasta 15 minutos; ver ADR-0010.

## Pendientes

- Implementar `security_db`, migraciones y repositorios.
- Implementar registro, login, refresh, logout y perfil.
- Configurar la cookie y `Cache-Control: no-store`.
- Implementar la validación de `Origin` en el gateway.
- Implementar el job de limpieza de sesiones.
- Añadir pruebas de CU-01 a CU-04 y CU-24.

## Referencias

- [CU-01 — Registro](../use-cases/cu-01-registro.md)
- [CU-02 — Inicio de sesión](../use-cases/cu-02-inicio-sesion.md)
- [CU-03 — Renovar sesión](../use-cases/cu-03-renovar-sesion.md)
- [CU-04 — Cerrar sesión](../use-cases/cu-04-cerrar-sesion.md)
- [CU-24 — Cambiar contraseña](../use-cases/cu-24-cambiar-contrasena.md)
- [ADR-0003 — Entrega de la clave pública JWT](0003-jwt-rs256.md)
- [ADR-0010 — Revocación de access tokens](0010-revocacion-access-tokens.md)
- [ADR-0011 — Hashing y política de contraseñas](0011-politica-contrasenas.md)
- [`security.md`](../security.md)
