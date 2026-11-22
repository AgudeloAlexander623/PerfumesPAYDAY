# CU-02 — Iniciar sesión

| Campo | Valor |
|---|---|
| Módulo | Autenticación |
| Actores | Visitante, Cliente y Administrador (principal), security-service (sistema) |
| Prioridad | Must |
| Diagrama | [`03-autenticacion`](../diagrams/03-autenticacion.svg) |

## Objetivo

Permitir que un usuario registrado demuestre su identidad y obtenga una sesión para acceder a las funciones protegidas: carrito persistente, checkout, historial de pedidos y panel administrativo.

## Precondiciones

- El usuario tiene una cuenta registrada y activa.
- El usuario no tiene una sesión iniciada en ese navegador, o su sesión expiró.

## Disparador

El usuario selecciona **Iniciar sesión** en el encabezado del sitio o al intentar acceder a una ruta protegida.

## Flujo principal

1. El sistema muestra el formulario con correo y contraseña.
2. El usuario ingresa sus credenciales.
3. El frontend valida que los campos no estén vacíos y que el correo tenga formato válido.
4. El frontend envía la solicitud al gateway por HTTPS.
5. El gateway enruta la petición a `security-service`.
6. `security-service` busca al usuario por correo en `security_db`.
7. `security-service` compara la contraseña recibida con el hash guardado usando una comparación de tiempo constante.
8. Si las credenciales son válidas, emite un **access token JWT** de 15 minutos y un **refresh token opaco** de 7 días de inactividad (máximo 30 días absolutos).
9. Guarda únicamente el **hash SHA-256** del refresh token y los datos de la sesión en `security_db`.
10. Responde `200` con el access token y los datos mínimos del usuario (`id`, `name`, `email`, `role`) y envía el refresh token en una cookie `HttpOnly` (`Set-Cookie`, `Cache-Control: no-store`).
11. El frontend guarda el access token en memoria y actualiza la interfaz.
12. Si existía un carrito de invitado, se ejecuta la fusión descrita en el [CU-15](cu-15-fusionar-carrito.md).
13. El sistema redirige según el rol: cliente al catálogo, administrador al panel.

## Flujos alternativos

### A1 — Credenciales inválidas

- **Cuándo ocurre:** el correo no existe o la contraseña no coincide.
- **Respuesta del sistema:** responde `401` con un mensaje genérico, sin indicar cuál dato falló. Registra el intento fallido.

### A2 — Demasiados intentos fallidos

- **Cuándo ocurre:** se supera el límite de intentos por cuenta o por IP en una ventana de tiempo.
- **Respuesta del sistema:** responde `429` e indica cuánto esperar antes de reintentar. No emite tokens.

### A3 — Cuenta deshabilitada

- **Cuándo ocurre:** el usuario existe pero está inactivo o bloqueado por un administrador.
- **Respuesta del sistema:** responde `403` con un mensaje neutro y no revela el estado interno de la cuenta.

### A4 — Datos incompletos o con formato inválido

- **Cuándo ocurre:** falta un campo o el correo no tiene formato válido.
- **Respuesta del sistema:** responde `400` e indica qué campos corregir.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `security-service` o la base de datos no responden.
- **Respuesta del sistema:** responde `503` con un mensaje genérico y permite reintentar.

## Postcondiciones

- El usuario queda autenticado y recibe sus tokens.
- El refresh token queda registrado en `security_db` asociado al usuario y al dispositivo.
- Se actualiza la fecha del último acceso.
- Si había un carrito de invitado, queda fusionado con el carrito del usuario.
- En caso de error no se emite ningún token ni se crea sesión.

## Reglas de negocio

- El correo se compara sin distinguir mayúsculas y minúsculas.
- El mensaje de error es siempre el mismo para correo inexistente y contraseña incorrecta (`401`).
- El rol se asigna/lee desde el servidor y nunca se acepta desde el cliente; se incluye en el token y en la respuesta mínima.
- Se permite más de una sesión activa: una por dispositivo.
- El access token dura 15 minutos; el refresh token dura 7 días por inactividad y 30 días de vida absoluta.
- El refresh token es opaco, se rota en cada uso y solo se persiste su hash SHA-256.
- Un inicio de sesión exitoso reinicia el contador de intentos fallidos.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidades:**
  - `users`: `id`, `name`, `email`, `password_hash`, `role`, `status`, `created_at`, `updated_at`, `last_login_at`.
  - `sessions`: `id`, `user_id`, `family_id`, `refresh_token_hash`, `expires_at`, `absolute_expires_at`, `revoked_at`, `replaced_by`, `user_agent`, `ip`, `created_at`, `last_used_at`.

## Seguridad

- Todo el tráfico viaja por HTTPS a través del gateway.
- La verificación de contraseñas usa **Argon2id** (comparación de tiempo constante).
- Los tokens nunca se escriben en logs ni se devuelven en la URL.
- El access token se mantiene en memoria; el refresh token opaco viaja en una cookie `HttpOnly` (`Secure` y nombre `__Host-` en producción, `SameSite=Lax`; ver [ADR-0009](../adr/0009-sesiones-refresh-cookies.md)).
- El gateway valida `Origin`/`Referer` en operaciones con cookie de refresh para prevenir CSRF.
- El límite de intentos protege contra fuerza bruta.
- El cierre de sesión revoca el refresh token correspondiente; el access token vigente expira como máximo en 15 minutos (ver [ADR-0010](../adr/0010-revocacion-access-tokens.md)).
- Las rutas de administración validan el rol `admin` en el servidor, no solo en la interfaz.

## Criterios de aceptación

- [ ] Un usuario registrado puede iniciar sesión con credenciales correctas.
- [ ] La respuesta incluye `id`, nombre y rol, pero nunca `password_hash`.
- [ ] Un correo inexistente y una contraseña incorrecta devuelven el mismo `401`.
- [ ] Superar el límite de intentos devuelve `429`.
- [ ] Una cuenta deshabilitada devuelve `403`.
- [ ] El access token expira y puede renovarse con el refresh token (CU-03).
- [ ] El inicio de sesión dispara la fusión del carrito de invitado cuando existe.
- [ ] El administrador es redirigido al panel y el cliente al catálogo.
- [ ] El flujo está cubierto por pruebas automatizadas de éxito y error.
