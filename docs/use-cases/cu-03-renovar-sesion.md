# CU-03 — Renovar sesión

| Campo | Valor |
|---|---|
| Módulo | Autenticación |
| Actores | Cliente y Administrador (principal), security-service (sistema) |
| Prioridad | Must |
| Diagrama | [`03-autenticacion`](../diagrams/03-autenticacion.svg) |

## Objetivo

Obtener un nuevo **access token** cuando el actual expira, sin obligar al usuario a escribir de nuevo sus credenciales.

## Precondiciones

- El usuario tiene una sesión activa con un **refresh token** válido.
- La cuenta está activa.

## Disparador

El frontend recibe un `401` por token expirado o detecta que el token está por vencer.

## Flujo principal

1. El frontend detecta que el access token expiró.
2. Envía la solicitud de renovación al gateway; el refresh token opaco viaja en la cookie `HttpOnly` (sin cuerpo ni URL).
3. El gateway valida `Origin`/`Referer` y enruta la petición a `security-service`.
4. `security-service` busca la sesión por el hash SHA-256 del refresh token.
5. Verifica que la sesión no esté expirada, revocada ni asociada a un usuario inactivo.
6. Revoca el refresh token usado y emite uno nuevo (**rotación atómica**).
7. Emite un nuevo access token (15 minutos) y actualiza la sesión.
8. Responde `200` con el nuevo access token, renueva la cookie del refresh token y envía `Cache-Control: no-store`.
9. El frontend reintenta una sola vez la petición original.

## Flujos alternativos

### A1 — Refresh token inválido o expirado

- **Cuándo ocurre:** el token no existe, ya expiró o fue revocado.
- **Respuesta del sistema:** responde `401`, limpia la sesión local y redirige al login.

### A2 — Reutilización de un refresh token ya rotado

- **Cuándo ocurre:** llega un token que ya fue reemplazado, lo que puede indicar robo.
- **Respuesta del sistema:** revoca todas las sesiones del usuario, responde `401` y exige un nuevo login.

### A3 — Usuario deshabilitado

- **Cuándo ocurre:** la cuenta fue bloqueada después de emitir la sesión.
- **Respuesta del sistema:** responde `403` y revoca la sesión.

### A4 — Renovaciones simultáneas

- **Cuándo ocurre:** varias peticiones reciben `401` al mismo tiempo.
- **Respuesta del sistema:** el frontend debe enviar una sola renovación y hacer que las demás esperen. Si llegan varias al servidor, solo una es válida.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `security-service` no responde.
- **Respuesta del sistema:** responde `503`; el frontend conserva la sesión y reintenta más tarde.

## Postcondiciones

- Existe una nueva pareja de tokens y el refresh anterior quedó revocado.
- La sesión registrada se actualiza con la nueva fecha de expiración.
- En A1 y A2 la sesión local se elimina; en A5 se conserva para reintentar.

## Reglas de negocio

- La rotación del refresh token es obligatoria en cada renovación.
- Cada dispositivo mantiene su propia sesión (`family_id`).
- La sesión tiene una vida absoluta de 30 días, aunque se renueve varias veces (inactividad: 7 días).
- Un refresh token revocado o ya rotado no puede volver a usarse; su reutilización revoca las sesiones del usuario.
- Renovar no requiere contraseña.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidad:** `sessions` con `id`, `user_id`, `family_id`, `refresh_token_hash`, `expires_at`, `absolute_expires_at`, `revoked_at`, `replaced_by`, `user_agent`, `ip`, `created_at`, `last_used_at`.

## Seguridad

- Refresh token opaco en cookie `HttpOnly`, `Secure` en producción (`SameSite=Lax`, nombre/`Path` según entorno; ver [ADR-0009](../adr/0009-sesiones-refresh-cookies.md)).
- Solo se guarda el hash SHA-256 del refresh token, nunca el valor completo.
- La reutilización de un token revocado/rotado revoca todas las sesiones del usuario.
- El gateway/servicio valida `Origin`/`Referer` para prevenir CSRF.
- Ningún token se escribe en logs. Respuestas de renovación con `Cache-Control: no-store`.

## Criterios de aceptación

- [ ] Un access token expirado se renueva sin pedir credenciales.
- [ ] El refresh token se rota en cada uso.
- [ ] Un refresh inválido devuelve `401` y cierra la sesión local.
- [ ] Reutilizar un refresh rotado revoca las sesiones del usuario.
- [ ] Una cuenta deshabilitada devuelve `403`.
- [ ] El flujo está cubierto por pruebas automatizadas.
