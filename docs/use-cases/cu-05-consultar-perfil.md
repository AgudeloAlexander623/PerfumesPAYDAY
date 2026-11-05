# CU-05 — Consultar perfil

| Campo | Valor |
|---|---|
| Módulo | Cuenta |
| Actores | Cliente (principal) |
| Prioridad | Should |
| Diagrama | — |

## Objetivo

Ver los datos básicos de la cuenta y el estado de la sesión.

## Precondiciones

- El usuario tiene una sesión activa.

## Disparador

El usuario selecciona **Mi perfil** en el menú de su cuenta.

## Flujo principal

1. El usuario abre **Mi perfil**.
2. El frontend solicita los datos al gateway.
3. El gateway enruta a `security-service`.
4. `security-service` busca al usuario por el `user_id` del token.
5. Devuelve nombre, correo, rol, fecha de registro y último acceso.
6. El frontend muestra la información y un acceso a las direcciones de envío (CU-16).

## Flujos alternativos

### A1 — Sesión expirada

- **Cuándo ocurre:** el access token ya no es válido.
- **Respuesta del sistema:** se ejecuta CU-03; si la renovación falla, se redirige al login.

### A2 — Usuario inexistente

- **Cuándo ocurre:** la cuenta fue eliminada después de emitir el token.
- **Respuesta del sistema:** responde `404`, cierra la sesión y redirige al login.

## Postcondiciones

- El usuario visualiza sus datos sin modificarlos.

## Reglas de negocio

- Solo se puede consultar el perfil propio.
- El correo es de solo lectura en la beta; cambiarlo requiere verificación y está fuera de alcance.
- El rol se muestra, pero no se puede editar.
- Las direcciones se consultan en CU-16 porque pertenecen a `order-service`.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidad:** `users`.

## Seguridad

- El `user_id` se toma del token, nunca de la URL.
- La respuesta nunca incluye `password_hash`.
- No se muestran identificadores internos de sesión.

## Criterios de aceptación

- [ ] El usuario ve su nombre, correo, rol y fechas de cuenta.
- [ ] La respuesta no incluye datos sensibles.
- [ ] Un usuario no puede consultar el perfil de otro.
- [ ] Si la sesión expiró, se intenta renovar antes de cerrar.
