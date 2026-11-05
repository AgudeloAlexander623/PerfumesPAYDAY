# CU-01 — Registrarse

| Campo | Valor |
|---|---|
| Módulo | Autenticación |
| Actores | Visitante (principal), security-service (sistema) |
| Prioridad | Must |
| Diagrama | [`03-autenticacion`](../diagrams/03-autenticacion.svg) |

## Objetivo

Permitir que una persona sin cuenta cree un usuario con rol `customer` para poder iniciar sesión y comprar.

## Precondiciones

- El visitante no tiene una sesión activa.
- El correo ingresado no está registrado.

## Disparador

El visitante selecciona **Crear cuenta** desde la pantalla de inicio de sesión o desde el encabezado del sitio.

## Flujo principal

1. El sistema muestra el formulario de registro.
2. El visitante ingresa nombre, correo y contraseña.
3. El frontend valida que los campos estén completos y que el correo tenga formato válido.
4. El frontend envía la solicitud al gateway.
5. El gateway enruta la solicitud a `security-service`.
6. `security-service` verifica que el correo no exista y asigna el rol `customer`.
7. `security-service` hashea la contraseña con Argon2 o bcrypt.
8. `security-service` guarda el usuario en `security_db`.
9. El servicio responde con el usuario creado, sin datos sensibles.
10. El frontend muestra el registro exitoso y lleva al visitante a iniciar sesión.

## Flujos alternativos

### A1 — El correo ya está registrado

- **Cuándo ocurre:** el correo ya existe en `security_db`.
- **Respuesta del sistema:** responde `409` con un mensaje neutro y sugiere iniciar sesión o recuperar la cuenta.

### A2 — Datos incompletos o con formato inválido

- **Cuándo ocurre:** falta un campo obligatorio o el correo no tiene formato válido.
- **Respuesta del sistema:** responde `400` e indica qué campos corregir, sin borrar lo ya escrito.

### A3 — Contraseña débil

- **Cuándo ocurre:** la contraseña no cumple la longitud o complejidad mínima.
- **Respuesta del sistema:** responde `422` y explica los requisitos antes de reenviar.

### A4 — Demasiados intentos

- **Cuándo ocurre:** se supera el límite de registros por IP o por correo.
- **Respuesta del sistema:** responde `429` y pide esperar antes de reintentar.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `security-service` o la base de datos no responden.
- **Respuesta del sistema:** responde `503` con un mensaje genérico y permite reintentar.

## Postcondiciones

- El usuario queda creado en `security_db` con rol `customer`.
- La contraseña queda guardada únicamente como hash.
- El visitante no obtiene sesión automáticamente; debe iniciar sesión.

## Reglas de negocio

- El correo es único y se guarda en minúsculas.
- El rol siempre es `customer`; el usuario no puede enviarlo ni cambiarlo.
- La contraseña nunca se guarda ni se devuelve en texto plano.
- El nombre es obligatorio y tiene una longitud máxima definida.
- El registro no confirma públicamente si un correo existe más allá del `409` estándar.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidad:** `users` con `id`, `name`, `email`, `password_hash`, `role`, `created_at`.

## Seguridad

- Validación de datos en el servidor con Pydantic, no solo en el frontend.
- Hash con Argon2 o bcrypt; nunca cifrado reversible.
- Límite de intentos por IP y por correo.
- Respuestas sin `password_hash` ni datos internos.
- Comunicación por HTTPS a través del gateway.
- Logs sin contraseñas ni tokens.

## Criterios de aceptación

- [ ] Un visitante puede registrarse con nombre, correo y contraseña válidos.
- [ ] El usuario creado tiene rol `customer`.
- [ ] La contraseña se almacena como hash.
- [ ] Un correo repetido devuelve `409` y no crea un segundo usuario.
- [ ] Los datos inválidos devuelven `400` o `422` con errores por campo.
- [ ] La respuesta nunca incluye `password_hash`.
- [ ] El límite de intentos devuelve `429`.
- [ ] El flujo está cubierto por al menos una prueba automatizada.
