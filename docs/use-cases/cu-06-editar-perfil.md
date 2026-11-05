# CU-06 — Editar perfil

| Campo | Valor |
|---|---|
| Módulo | Cuenta |
| Actores | Cliente (principal) |
| Prioridad | Could |
| Diagrama | — |

## Objetivo

Permitir que el usuario actualice su nombre visible.

## Precondiciones

- El usuario tiene una sesión activa.

## Disparador

El usuario selecciona **Editar** en la pantalla de su perfil.

## Flujo principal

1. El usuario abre **Mi perfil** y selecciona **Editar**.
2. El formulario muestra el nombre actual.
3. El usuario modifica el nombre y guarda.
4. El frontend valida que no esté vacío ni supere la longitud máxima.
5. Envía la solicitud al gateway y este la enruta a `security-service`.
6. `security-service` actualiza únicamente los campos permitidos del usuario del token.
7. Devuelve el perfil actualizado y el frontend lo muestra.

## Flujos alternativos

### A1 — Nombre inválido

- **Cuándo ocurre:** está vacío o excede la longitud permitida.
- **Respuesta del sistema:** responde `400` o `422` con el campo a corregir.

### A2 — Intento de modificar otro campo

- **Cuándo ocurre:** el cliente envía `email`, `role` o `id` en el cuerpo.
- **Respuesta del sistema:** el servidor ignora esos campos y solo actualiza los permitidos.

### A3 — Sesión expirada

- **Cuándo ocurre:** el token ya no es válido.
- **Respuesta del sistema:** se ejecuta CU-03; si falla, se redirige al login.

## Postcondiciones

- El nombre del usuario queda actualizado.
- El resto de los datos permanece igual.

## Reglas de negocio

- En la beta solo se puede editar el nombre.
- El correo, el rol y el identificador son inmutables desde este flujo.
- Cambiar contraseña es un caso aparte (CU-24).
- Cambiar el correo requiere verificación y queda fuera del alcance.

## Datos y servicios involucrados

- **Servicio:** `security-service`.
- **Base de datos:** `security_db`.
- **Entidad:** `users`.

## Seguridad

- El `user_id` se toma del token.
- Se aplica una lista blanca de campos editables para evitar asignación masiva.
- Se valida la longitud y el contenido en el servidor.

## Criterios de aceptación

- [ ] El usuario puede cambiar su nombre.
- [ ] Los campos no permitidos se ignoran.
- [ ] Un nombre inválido devuelve `400` o `422`.
- [ ] El cambio se refleja en la siguiente consulta del perfil.
