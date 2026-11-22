# CU-24 — Cambiar contraseña

| Campo | Valor |
|---|---|
| Módulo | Cuenta |
| Actores | Cliente y Administrador (principal), security-service (sistema) |
| Prioridad | Should |
| Diagrama | — |

## Objetivo

Permitir que el usuario cambie su contraseña conociendo la actual, sin depender del envío de correos.

## Precondiciones

- El usuario tiene una sesión activa.

## Disparador

El usuario selecciona **Cambiar contraseña** en su perfil.

## Flujo principal

1. El frontend muestra los campos: contraseña actual, nueva y confirmación.
2. El usuario completa el formulario.
3. El frontend valida que la nueva contraseña y la confirmación coincidan.
4. Envía la solicitud al gateway y este la enruta a `security-service`.
5. `security-service` verifica la contraseña actual contra el hash guardado.
6. Valida que la nueva cumpla la política de seguridad (12–128 caracteres, no común, no igual al correo/nombre y distinta de la actual).
7. Hashea la nueva contraseña con **Argon2id** y actualiza el usuario.
8. Revoca todas las sesiones del usuario, incluida la actual.
9. Responde `204` con `Cache-Control: no-store` y el frontend redirige al login.

## Flujos alternativos

### A1 — Contraseña actual incorrecta

- **Cuándo ocurre:** el hash no coincide.
- **Respuesta del sistema:** responde `401` con un mensaje genérico y registra el intento.

### A2 — Contraseña nueva débil

- **Cuándo ocurre:** no cumple la política de seguridad o está en la lista de contraseñas comunes.
- **Respuesta del sistema:** responde `422` con código `WEAK_PASSWORD` y explica los requisitos.

### A3 — Contraseña nueva igual a la actual

- **Cuándo ocurre:** el usuario repite la misma contraseña.
- **Respuesta del sistema:** responde `400` con código `PASSWORD_REUSED` y pide una diferente.

### A4 — Demasiados intentos

- **Cuándo ocurre:** se supera el límite de intentos.
- **Respuesta del sistema:** responde `429` y pide esperar.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `security-service` no responde.
- **Respuesta del sistema:** responde `503`; la contraseña actual no cambia.

## Postcondiciones

- La contraseña queda actualizada como hash.
- Todas las sesiones quedan revocadas y el usuario debe iniciar sesión de nuevo.

## Reglas de negocio

- Siempre se exige la contraseña actual.
- La nueva contraseña debe tener entre 12 y 128 caracteres, no recortarse, no ser común y no ser igual al correo o al nombre.
- La nueva contraseña no puede ser igual a la anterior.
- No se guarda historial de contraseñas en la beta.
- No se envía la contraseña por correo.
- Cambiar la contraseña revoca todas las sesiones por seguridad y exige un nuevo inicio de sesión.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidades:** `users`, `sessions`.

## Seguridad

- Verificación de contraseña con **Argon2id** (comparación de tiempo constante).
- Hash de la nueva contraseña con **Argon2id** (ver [ADR-0011](../adr/0011-politica-contrasenas.md)).
- Límite de intentos por usuario e IP.
- La contraseña nunca se escribe en logs ni se devuelve en la respuesta.
- La revocación de sesiones impide que el refresh token siga activo; el access token vigente expira como máximo en 15 minutos (ver [ADR-0010](../adr/0010-revocacion-access-tokens.md)).

## Criterios de aceptación

- [ ] El usuario puede cambiar su contraseña con la actual correcta.
- [ ] Una contraseña actual incorrecta devuelve `401`.
- [ ] Una contraseña débil devuelve `422`.
- [ ] Repetir la contraseña actual devuelve `400`.
- [ ] Todas las sesiones quedan revocadas.
- [ ] La nueva contraseña funciona en el siguiente login.
