# ADR-0011 — Hashing y política de contraseñas

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-14 |
| Decisores | Equipo, responsable de seguridad |
| Relacionados | CU-01, CU-02, CU-24, [ADR-0009](0009-sesiones-refresh-cookies.md), [`security.md`](../security.md) |

## Contexto

El registro, el inicio de sesión y el cambio de contraseña necesitan una política común. Si cada endpoint valida distinto, el frontend muestra mensajes inconsistentes y las pruebas de seguridad no tienen un criterio único.

También hay que elegir el algoritmo de hashing. La beta es académica, pero debe resistir revisiones básicas de seguridad y no almacenar contraseñas de forma reversible.

## Decisión

### 1. Algoritmo

- **Argon2id** mediante `argon2-cffi`.
- Parámetros iniciales:
  - `time_cost = 3`
  - `memory_cost = 65536` KiB (64 MiB)
  - `parallelism = 1`
  - `hash_len = 32`
  - `salt_len = 16`
- La verificación la hace `PasswordHasher.verify`, que compara en tiempo constante.
- Si al iniciar sesión el hash usa parámetros distintos a los actuales, se **rehashea** con los parámetros vigentes y se actualiza el registro.
- El hash incluye algoritmo, parámetros y sal; se guarda como texto en `users.password_hash`.
- Nunca se usa cifrado reversible, MD5, SHA-1, SHA-256 solo ni “hash + sal” manual.

Los parámetros se ajustan si el contenedor tiene poca memoria; el mínimo aceptable es el de OWASP (`m=19456`, `t=2`, `p=1`). No se baja de ahí.

### 2. Política

| Regla | Valor |
|---|---|
| Longitud mínima | 12 caracteres |
| Longitud máxima | 128 caracteres |
| Caracteres permitidos | Unicode, incluidos espacios internos |
| Composición obligatoria | Ninguna (se prioriza longitud sobre complejidad) |
| Recorte | No se recorta la contraseña; se valida tal como llega |
| Igual al correo | Rechazada (comparación sin distinguir mayúsculas) |
| Igual al nombre | Rechazada (comparación sin distinguir mayúsculas) |
| Lista de contraseñas comunes | Rechazada; lista local de al menos 1.000 valores |
| Solo espacios | Rechazada |
| Repetir la actual | Rechazada en el cambio de contraseña |

La política sigue la recomendación de longitud y bloqueo de contraseñas comunes de NIST SP 800-63B. No se exigen mayúsculas, números y símbolos obligatorios porque producen contraseñas predecibles y peores.

La lista de contraseñas comunes vive en `security-service` como recurso local, sin llamadas externas. No se registra la contraseña ni el motivo exacto de rechazo en logs.

### 3. Respuestas

- Contraseña débil o en la lista de comunes → `422` con código `WEAK_PASSWORD` y detalle por campo.
- Contraseña que no cumple el tipo o la longitud extrema → `400` con código `VALIDATION_ERROR`.
- Contraseña actual incorrecta en el cambio → `401` genérico.
- Contraseña nueva igual a la actual → `400` con código `PASSWORD_REUSED`.
- La respuesta nunca devuelve la contraseña ni el hash.

### 4. Cambio de contraseña

1. Exigir la contraseña actual.
2. Validar la nueva con la misma política del registro.
3. Rechazar si es igual a la actual.
4. Hashear y actualizar.
5. Revocar todas las sesiones del usuario según [ADR-0009](0009-sesiones-refresh-cookies.md).
6. Responder `204`.
7. Exigir un nuevo inicio de sesión.

### 5. Límites y abuso

- Login y cambio de contraseña tienen rate limit por IP y por cuenta.
- Los intentos fallidos se cuentan por cuenta y por IP; un login exitoso reinicia el contador.
- Tras superar el umbral se responde `429` con `Retry-After`.
- El bloqueo es temporal; no se bloquea la cuenta de forma permanente desde el login.
- Umbral inicial confirmado para la beta: 5 intentos fallidos por cuenta/IP y bloqueo de 15 minutos, configurable con `LOGIN_MAX_FAILED_ATTEMPTS` y `LOGIN_LOCKOUT_MINUTES`.
- Los intentos fallidos se registran sin contraseña, sin hash y sin token.

### 6. Datos y pruebas

- `users.password_hash` es `text not null`; nunca se selecciona en las respuestas.
- Las pruebas deben cubrir: hash distinto por sal, verificación correcta, contraseña incorrecta, contraseña débil, contraseña común, contraseña igual al correo, rehash y cambio con revocación de sesiones.
- Una prueba de integración debe verificar que `password_hash` nunca aparece en la API.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| bcrypt | Maduro y simple | Límite de 72 bytes y menos resistente a GPU | Válido, pero Argon2id es mejor |
| Argon2id | Resistente a GPU/ASIC; recomendado por OWASP | Más memoria por hash | **Aceptado** |
| PBKDF2 | Disponible en la librería estándar | Menos resistente a GPU | Rechazado |
| SHA-256 con sal | Rápido | Inadecuado para contraseñas | Rechazado |
| Composición obligatoria | Familiar para usuarios | Contraseñas predecibles; mala práctica actual | Rechazado |

## Consecuencias

- `security-service` necesita `argon2-cffi` y una lista local de contraseñas comunes.
- El registro y el cambio de contraseña comparten el mismo validador.
- El frontend puede mostrar la política antes de enviar, pero el servidor siempre revalida.
- El coste de 64 MiB por hash limita la concurrencia; se mide en la prueba de carga de la beta.

## Pendientes

- Agregar `argon2-cffi` a `pyproject.toml`.
- Crear el validador compartido y la lista de contraseñas comunes.
- Implementar el rehash al iniciar sesión.
- Añadir las pruebas de la sección 6.
- Medir memoria y latencia con 10 logins concurrentes.

## Referencias

- [CU-01 — Registro](../use-cases/cu-01-registro.md)
- [CU-02 — Inicio de sesión](../use-cases/cu-02-inicio-sesion.md)
- [CU-24 — Cambiar contraseña](../use-cases/cu-24-cambiar-contrasena.md)
- [ADR-0009 — Sesiones, refresh tokens y cookies](0009-sesiones-refresh-cookies.md)
- [`security.md`](../security.md)
- [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
