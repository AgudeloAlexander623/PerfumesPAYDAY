# ADR-0010 — Revocación de access tokens y revalidación de privilegios

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-14 |
| Decisores | Equipo, responsable de seguridad |
| Relacionados | CU-03, CU-04, CU-20 a CU-25, [ADR-0003](0003-jwt-rs256.md), [ADR-0009](0009-sesiones-refresh-cookies.md), [`security.md`](../security.md) |

## Contexto

Los access tokens JWT son stateless: una vez firmados, cualquier servicio con la clave pública puede validarlos hasta que expiren. Eso es deseable para el rendimiento, pero plantea dos preguntas:

1. ¿Qué pasa con el access token después de cerrar sesión o cambiar la contraseña?
2. ¿Qué pasa si a un usuario se le retira el rol `admin` o se le deshabilita la cuenta?

Sin una decisión explícita, el equipo podría terminar implementando una denylist por request, un chequeo de base de datos en cada petición o, peor, asumir que el token se invalida solo.

## Decisión

### 1. Access tokens de vida corta, sin denylist en la beta

- El access token dura **15 minutos** y no se consulta en una denylist en cada petición.
- Cerrar sesión, rotar el refresh token o cambiar la contraseña **no revocan el access token actual**; dejan de emitir refresh tokens nuevos.
- El riesgo residual queda acotado a la ventana de 15 minutos y se documenta en [`security.md`](../security.md).
- `jti` es obligatorio y se registra en logs/auditoría para trazabilidad, pero no se usa para bloquear tokens en la beta.

Esta decisión evita convertir cada petición autenticada en una consulta a base de datos o a Redis, y mantiene la validación del gateway sin estado.

### 2. Revocación de sesiones

- Logout revoca la sesión actual (refresh token) y elimina la cookie.
- Logout-all revoca todas las sesiones del usuario.
- Cambiar la contraseña revoca todas las sesiones.
- Deshabilitar una cuenta revoca todas sus sesiones.
- En todos los casos, el access token ya emitido expira como máximo en 15 minutos.

### 3. Privilegios y estado de la cuenta

Para la beta, la autorización se basa en los claims `roles` y `sub` del access token:

- El gateway valida el rol `admin` antes de proxificar rutas administrativas.
- `catalog` y `orders` vuelven a validar el rol en el token, como defensa en profundidad.
- Un cambio de rol o una deshabilitación surte efecto, como máximo, cuando expira el access token o cuando se revocan las sesiones.
- No se consulta `security_db` en cada petición; hacerlo rompería el aislamiento de bases y añadiría latencia.

> Esta es una decisión consciente para la beta. Si el proyecto exige revocación inmediata, se implementa `token_version` o una denylist de `jti` en una fase posterior, no en medio de la beta.

### 4. Camino de evolución

Si más adelante se necesita revocación inmediata:

| Opción | Mecanismo | Coste |
|---|---|---|
| `token_version` | Claim con la versión del usuario; se compara contra un valor en caché | Requiere caché y coordinación |
| Denylist de `jti` | Redis con TTL igual a la vida del token | Requiere Redis y una consulta por request |
| Introspección | El gateway pregunta a `security-service` | Acopla el gateway al emisor y añade latencia |

No se implementa ninguna en la beta. La decisión se revisa si aparece un requisito de seguridad que lo justifique.

### 5. Respuestas de error

- `401` cuando falta el token, la firma es inválida, el token expiró o `typ` no es `access`.
- `403` cuando el token es válido pero el rol no alcanza.
- `401` incluye `WWW-Authenticate: Bearer` y, cuando aplique, `error="invalid_token"`.
- `403` puede incluir `error="insufficient_scope"`.
- El cuerpo sigue el envelope de [ADR-0006](0006-errores-paginacion-idempotencia.md).

### 6. Pruebas obligatorias

- Token expirado → `401`.
- Firma inválida → `401`.
- `alg` distinto de RS256 → `401`.
- `typ` distinto de `access` → `401`.
- `roles` vacío en una ruta protegida → `401` o `403` según el guard.
- Cliente en ruta admin → `403`.
- Logout revoca el refresh y el refresh ya no sirve.
- Cambio de contraseña revoca todas las sesiones.
- El access token anterior sigue funcionando hasta expirar (comportamiento documentado).

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| Denylist de `jti` por request | Revocación inmediata | Redis, latencia y estado | Fuera de la beta |
| `token_version` por usuario | Revocación casi inmediata y barata | Requiere caché y un claim extra | Evolución futura |
| Introspección en cada request | Fuente única de verdad | Acopla gateway y emisor; latencia | Rechazada |
| Access tokens de 15 min sin denylist | Simple, stateless y suficiente para la beta | Ventana de exposición de 15 min | **Aceptada** |

## Consecuencias

- El logout es inmediato para el refresh, pero no para el access token.
- El frontend debe dejar de usar el access token al cerrar sesión y no confiar solo en el borrado local.
- Las pruebas deben verificar el comportamiento documentado para no reportarlo como bug.
- La decisión se revisa si el profesor o el equipo exige revocación inmediata.

## Pendientes

- Implementar `WWW-Authenticate` en las respuestas `401`.
- Validar `typ: "access"` en el verificador de Node.
- Añadir las pruebas de la sección 6.
- Documentar la ventana de 15 minutos en la guía de seguridad y en la demo.

## Referencias

- [CU-03 — Renovar sesión](../use-cases/cu-03-renovar-sesion.md)
- [CU-04 — Cerrar sesión](../use-cases/cu-04-cerrar-sesion.md)
- [CU-20 — Gestionar productos](../use-cases/cu-20-gestionar-productos.md)
- [CU-23 — Auditar acciones](../use-cases/cu-23-auditar-acciones.md)
- [CU-24 — Cambiar contraseña](../use-cases/cu-24-cambiar-contrasena.md)
- [ADR-0003 — Entrega de la clave pública JWT](0003-jwt-rs256.md)
- [ADR-0009 — Sesiones, refresh tokens y cookies](0009-sesiones-refresh-cookies.md)
- [`security.md`](../security.md)
