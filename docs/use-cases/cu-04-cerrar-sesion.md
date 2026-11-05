# CU-04 — Cerrar sesión

| Campo | Valor |
|---|---|
| Módulo | Autenticación |
| Actores | Cliente y Administrador (principal), security-service (sistema) |
| Prioridad | Must |
| Diagrama | [`03-autenticacion`](../diagrams/03-autenticacion.svg) |

## Objetivo

Terminar la sesión actual y revocar sus tokens para que no puedan reutilizarse.

## Precondiciones

- Existe una sesión iniciada o al menos una cookie de refresh token.

## Disparador

El usuario selecciona **Cerrar sesión**.

## Flujo principal

1. El usuario selecciona **Cerrar sesión**.
2. El frontend envía la solicitud al gateway.
3. El gateway enruta la petición a `security-service`.
4. `security-service` identifica la sesión por el refresh token.
5. Marca la sesión como revocada y elimina la cookie.
6. El frontend borra el access token de memoria y los datos del usuario.
7. El sistema redirige al inicio o al login.

## Flujos alternativos

### A1 — No hay sesión activa

- **Cuándo ocurre:** la sesión ya expiró o fue revocada.
- **Respuesta del sistema:** responde `204` igualmente y limpia el estado local. El cierre de sesión es idempotente.

### A2 — Falla la red o el servicio

- **Cuándo ocurre:** no se puede contactar a `security-service`.
- **Respuesta del sistema:** el frontend limpia la sesión local de todas formas. El token del servidor expirará por tiempo.

### A3 — Cerrar sesión en todos los dispositivos

- **Cuándo ocurre:** el usuario elige esta opción desde su perfil.
- **Respuesta del sistema:** `security-service` revoca todas las sesiones del `user_id` y responde `204`. El dispositivo actual también queda desconectado.

## Postcondiciones

- La sesión actual queda revocada y la cookie eliminada.
- El frontend no conserva tokens ni datos del usuario.
- El carrito guardado en el servidor y los pedidos **no** se eliminan.
- En A3, todas las sesiones del usuario quedan revocadas.

## Reglas de negocio

- El cierre de sesión nunca elimina el carrito ni el historial.
- El carrito de invitado no se conserva después de cerrar sesión; el carrito autenticado permanece en `order-service`.
- La operación es idempotente: repetirla no genera error.
- Cerrar sesión en todos los dispositivos requiere una sesión válida en el dispositivo actual.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidad:** `sessions`.

## Seguridad

- El refresh token se revoca en el servidor, no solo se borra en el navegador.
- La cookie se elimina con las mismas propiedades con que se creó.
- No se registran tokens en logs.
- A3 permite responder ante la pérdida de un dispositivo.

## Criterios de aceptación

- [ ] Cerrar sesión revoca el refresh token en la base de datos.
- [ ] El frontend queda sin tokens ni datos de usuario.
- [ ] Repetir el cierre de sesión devuelve `204`.
- [ ] El carrito y los pedidos siguen existiendo después del cierre.
- [ ] La opción "cerrar en todos los dispositivos" revoca todas las sesiones.
