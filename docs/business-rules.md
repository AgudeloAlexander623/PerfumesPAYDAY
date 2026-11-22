# Reglas de negocio

Documento central de reglas de negocio de **Perfumes GOLD**. Consolida y normaliza las reglas definidas en los [casos de uso](use-cases/README.md), los [ADR](adr/README.md), los [contratos de API](api/README.md) y la documentación de [seguridad](security.md) y [arquitectura](architecture.md).

> **Estado:** borrador vivo. Si una regla cambia, se actualiza primero el caso de uso/ADR correspondiente y luego este documento en el mismo cambio.  
> **Última actualización:** 2026-11-16

---

## 1. Alcance y fuentes

| Fuente | Uso |
|---|---|
| [Casos de uso](use-cases/README.md) | Comportamiento funcional, pre/postcondiciones y reglas por flujo. |
| [ADR](adr/README.md) | Decisiones técnicas que fijan reglas (tokens, sesiones, errores, contraseñas, etc.). |
| [`api/security.openapi.yaml`](api/security.openapi.yaml) | Contrato de autenticación y cuenta (borrador, Fase 1). |
| [`security.md`](security.md) | Controles y políticas de seguridad aplicables como reglas. |

**Dependencias abiertas:** [ADR-0004](adr/0004-propiedad-datos.md) (propiedad de datos de catálogo/pedidos) y [ADR-0005](adr/0005-comunicacion-interna.md) (comunicación `orders` → `catalog`) pueden detallar reglas operativas de esos dominios sin invalidar las reglas funcionales aquí descritas.

---

## 2. Reglas transversales

### 2.1 Identidad, autorización y propiedad de datos
- **RN-T01 — Identidad desde el token:** el `user_id`, el rol y el contexto de autenticación se obtienen del access token validado en el servidor; nunca del cuerpo, query string ni ruta enviados por el cliente.
- **RN-T02 — Acceso al recurso propio:** un usuario solo puede consultar/modificar sus propios recursos (perfil, carrito, direcciones, pedidos). Las consultas filtran por propietario en la misma operación de datos.
- **RN-T03 — No revelar existencia:** ante un recurso inexistente o ajeno, se responde `404` (no `403`) cuando corresponda para no confirmar su existencia (p. ej. ítems, direcciones o pedidos ajenos).
- **RN-T04 — Autorización por rol en servidor:** las rutas administrativas requieren rol `admin` validado en gateway y en el servicio; la interfaz no es un control de seguridad.
- **RN-T05 — Lista blanca de campos:** las actualizaciones solo aceptan/ignoran campos permitidos; no se permite modificar `id`, `role`, `email` u otros campos no autorizados desde flujos que no lo permitan.

### 2.2 Errores, validación y abuso
- **RN-T06 — Envelope de error uniforme:** las respuestas de error siguen `error{code,message,details?,requestId?}` según [ADR-0006](adr/0006-errores-paginacion-idempotencia.md).
- **RN-T07 — Semántica HTTP:** `400` formato/tipo/parámetros inválidos; `401` autenticación inválida o ausente; `403` sin permiso, cuenta deshabilitada o CSRF inválido; `404` inexistente/ajeno; `409` conflicto de negocio/idempotencia; `422` regla de negocio incumplida; `429` rate limit; `503` dependencia no disponible.
- **RN-T08 — Validación en servidor:** el frontend puede validar para UX, pero el servidor valida y decide siempre.
- **RN-T09 — Sin datos sensibles en respuestas/logs:** no se exponen ni registran contraseñas, `password_hash`, tokens, datos de tarjeta ni secretos.

### 2.3 Precios, moneda y snapshots
- **RN-T10 — Moneda:** los precios y totales se expresan en pesos colombianos (COP).
- **RN-T11 — Precio/stock de referencia:** el precio y stock mostrados en catálogo/carrito son referenciales; se revalidan en operaciones críticas (carrito autenticado/checkout).
- **RN-T12 — Cálculo en servidor:** los totales definitivos (carrito autenticado y pedido) se calculan en el servidor; el cliente no es fuente de verdad.
- **RN-T13 — Inmutabilidad de pedidos:** los pedidos guardan una copia (snapshot) de productos, precios, totales y dirección al momento de la compra; cambios posteriores no los alteran.

### 2.4 Idempotencia
- **RN-T14 — Operaciones idempotentes declaradas:** `POST /api/v1/orders` y `POST /api/v1/cart/merge` requieren `Idempotency-Key` (UUID v4). Misma clave + mismo cuerpo devuelve la respuesta guardada; misma clave + cuerpo distinto devuelve `409` `IDEMPOTENCY_CONFLICT` (ADR-0006).
- **RN-T15 — Logout idempotente:** cerrar sesión responde `204` aunque no exista una sesión activa.

---

## 3. Autenticación y sesiones (CU-01 a CU-04)

| ID | Regla | Fuente |
|---|---|---|
| RN-A01 | Registro público con `name`, `email`, `password`; crea usuario con rol `customer` y estado `active`, sin iniciar sesión automáticamente. | CU-01, ADR-0009 |
| RN-A02 | `email` único, normalizado a minúsculas; el rol lo asigna el servidor y nunca se acepta del cliente. | CU-01, CU-02 |
| RN-A03 | `name` obligatorio, 1–120 caracteres. | CU-01, CU-06, ADR-0009 |
| RN-A04 | Contraseña: 12–128 caracteres, sin recorte, no común y no igual a correo/nombre (sin composición obligatoria). Incumplimiento de política → `422 WEAK_PASSWORD`. | CU-01, ADR-0011 |
| RN-A05 | Contraseñas se almacenan solo como hash **Argon2id**; nunca en texto plano ni cifrado reversible. | ADR-0011, security.md |
| RN-A06 | Registro con correo existente → `409` con mensaje neutro. Datos mal formados/tipo → `400`; regla de negocio de contraseña → `422`. | CU-01, ADR-0006 |
| RN-A07 | Login valida credenciales con comparación de tiempo constante; correo inexistente o contraseña incorrecta → `401` genérico (`INVALID_CREDENTIALS`). | CU-02, ADR-0011 |
| RN-A08 | Cuenta deshabilitada → `403` (`ACCOUNT_DISABLED`) sin revelar estado interno. | CU-02 |
| RN-A09 | Access token: JWT RS256, 15 minutos, claims obligatorios (`sub`, `iss`, `aud`, `iat`, `exp`, `jti`, `roles`, `typ: "access"`), devuelto en cuerpo y mantenido en memoria por el cliente. | ADR-0003, ADR-0009, ADR-0010 |
| RN-A10 | Refresh token: opaco (32 bytes, CSPRNG), solo en cookie `HttpOnly` (`Secure`/`__Host-` en prod, `SameSite=Lax`), nunca en cuerpo/URL/logs; en BD solo hash SHA-256. | ADR-0009 |
| RN-A11 | Sesión: rotación obligatoria en cada refresh; 7 días por inactividad y 30 días de vida absoluta; se permite una sesión por dispositivo. | CU-02, CU-03, ADR-0009 |
| RN-A12 | Reutilización de refresh revocado/rotado → revoca sesiones del usuario y responde `401` (`INVALID_REFRESH_TOKEN`). | CU-03, ADR-0009 |
| RN-A13 | `POST /api/v1/auth/refresh` y `POST /api/v1/auth/logout` validan `Origin/Referer` (CSRF) cuando usan cookie; en producción, ausencia de ambos → `403` (`CSRF_VALIDATION_FAILED`). | ADR-0009, contrato |
| RN-A14 | Logout revoca la sesión de refresh y elimina la cookie; `?all=true` revoca todas las sesiones y requiere bearer válido. No elimina carrito ni historial. | CU-04, ADR-0009 |
| RN-A15 | Revocación diferida del access token: logout/cambio de contraseña/deshabilitación revocan sesiones, pero el access token ya emitido puede ser válido hasta expirar (máx. 15 min). | ADR-0010 |
| RN-A16 | Rate limit en registro/login/refresh/cambio de contraseña por IP y/o cuenta; exceso → `429` con `Retry-After`. | CU-01..04, CU-24, ADR-0011 |

---

## 4. Cuenta y contraseñas (CU-05, CU-06, CU-24)

| ID | Regla | Fuente |
|---|---|---|
| RN-C01 | El usuario solo puede consultar y editar su propio perfil (`GET/PATCH /api/v1/users/me`), identificado por `sub` del token. | CU-05, CU-06 |
| RN-C02 | Perfil expone datos públicos: `id`, `name`, `email`, `role`, `status`, `createdAt`, `updatedAt`, `lastLoginAt`; nunca `passwordHash` ni datos internos de sesión. | CU-05, contrato |
| RN-C03 | En la beta solo `name` es editable (1–120 caracteres); `email`, `role`, `status`, `id` son inmutables en este flujo y campos no permitidos se ignoran. | CU-06 |
| RN-C04 | Cambio de correo requiere verificación y está fuera del alcance de la beta. | CU-05, CU-06 |
| RN-C05 | Cambio de contraseña (`PATCH /api/v1/users/me/password`) exige contraseña actual, valida política y rechaza si la nueva es igual a la actual (`400 PASSWORD_REUSED`). | CU-24, ADR-0011 |
| RN-C06 | Contraseña actual incorrecta → `401`; nueva débil/común → `422 WEAK_PASSWORD`. | CU-24, ADR-0011 |
| RN-C07 | Al cambiar la contraseña se actualiza el hash (Argon2id), se revocan todas las sesiones y se responde `204` (el cliente debe iniciar sesión nuevamente). | CU-24, ADR-0009 |

---

## 5. Catálogo (CU-07 a CU-10)

| ID | Regla | Fuente |
|---|---|---|
| RN-K01 | El catálogo, búsqueda y detalle son públicos (no requieren sesión). | CU-07, CU-08, CU-09 |
| RN-K02 | Solo se muestran al público productos con estado `active`; un producto inactivo devuelve `404` en detalle público. | CU-07, CU-09 |
| RN-K03 | El precio mostrado es de referencia y corresponde a la presentación (variante); se revalida en checkout. | CU-07, CU-09, CU-17 |
| RN-K04 | Listados paginados con tamaño por defecto y máximo (ver ADR-0006 para convención de paginación). | CU-07, ADR-0006 |
| RN-K05 | Búsqueda/filtros: texto parcial sin distinguir mayúsculas; filtros combinados con **Y**; filtros reproducibles en URL; parámetros validados en servidor. | CU-08 |
| RN-K06 | Consultas parametrizadas/ORM (sin concatenación SQL) y escape al renderizar para prevenir inyección/XSS. | CU-08, security.md |
| RN-K07 | Cada presentación tiene precio y stock propios; la presentación elegida (no el producto genérico) es la que se agrega al carrito. | CU-09, CU-11 |
| RN-K08 | Si no hay stock disponible, no se permite agregar al carrito desde el detalle. | CU-09 |
| RN-K09 | La página de mayoristas es informativa/estática (“Próximamente”), sin flujo B2B, sin captura de datos ni precios mayoristas en la beta. | CU-10 |

---

## 6. Carrito (CU-11 a CU-15)

| ID | Regla | Fuente |
|---|---|---|
| RN-R01 | Carrito de invitado: vive en el navegador (solo `variant_id` y cantidad, sin precios); carrito autenticado: persiste en `order-service` asociado al `user_id` del token. | CU-11, CU-12 |
| RN-R02 | El usuario no puede leer/escribir el carrito de otro usuario. | CU-11, CU-12, CU-13, CU-14 |
| RN-R03 | Cantidad es entero positivo; la cantidad máxima por ítem es `min(stock, límite de negocio)`. Exceso/valor inválido se rechaza (`409` por stock, `400` por formato/rango según aplique). | CU-11, CU-13 |
| RN-R04 | Agregar un producto/presentación repetida suma cantidades (sin duplicar filas), respetando el tope. | CU-11, CU-15 |
| RN-R05 | Carrito autenticado revalida existencia, estado activo y stock con `catalog-service`; no se guarda un ítem sin validar cuando el servicio no está disponible (`503`). | CU-11, CU-13 |
| RN-R06 | Totales mostrados: carrito de invitado informativo en cliente; carrito autenticado calculado en servidor con datos vigentes. El total definitivo se fija en checkout. | CU-12 |
| RN-R07 | No se puede continuar al checkout con ítems inválidos (sin stock, inactivos o inconsistentes). | CU-12 |
| RN-R08 | Cantidad 0 al actualizar se interpreta como eliminación (CU-14). Eliminar el último ítem deja el carrito vacío pero existente. Eliminación idempotente. | CU-13, CU-14 |
| RN-R09 | Fusión al login (CU-15): combina carrito invitado y autenticado, suma con tope de stock, omite ítems no disponibles informando el motivo, es idempotente (`Idempotency-Key`) y solo borra el carrito local si la fusión es exitosa. Tras fusionar, el servidor es la fuente de verdad. | CU-15, ADR-0006 |

---

## 7. Direcciones, checkout y pedidos (CU-16 a CU-19)

| ID | Regla | Fuente |
|---|---|---|
| RN-P01 | Direcciones pertenecen al usuario autenticado (`user_id` del token); solo el dueño puede listarlas/crearlas/editarlas/eliminarlas. | CU-16 |
| RN-P02 | Máximo una dirección predeterminada por usuario; la primera dirección creada queda como predeterminada. El cambio de predeterminada se realiza de forma consistente. | CU-16 |
| RN-P03 | Departamento y ciudad se validan contra la lista de Colombia; teléfono se guarda como texto. Datos inválidos → `400/422`. Límite de direcciones → `409`. | CU-16 |
| RN-P04 | Los pedidos guardan una copia de la dirección usada; editar/eliminar la dirección actual no altera pedidos anteriores. | CU-16, CU-17, CU-19 |
| RN-P05 | Checkout requiere sesión, carrito con ítems válidos, dirección propia y `Idempotency-Key`; el servidor revalida precio/stock y calcula totales. | CU-17, ADR-0006 |
| RN-P06 | Cambio de precio o stock insuficiente/invalidez en checkout → `409`, no se crea pedido y el carrito se conserva para corrección. Dirección ajena/inexistente → `404`. | CU-17 |
| RN-P07 | Creación de pedido, descuento de stock y registro asociado deben ser consistentes (transacción/compensación): no se permiten pedidos parciales ante fallos. | CU-17 |
| RN-P08 | Reintento con la misma clave de idempotencia no duplica el pedido; devuelve el resultado ya creado. | CU-17, ADR-0006 |
| RN-P09 | El pago es simulado en la beta: no se solicitan ni almacenan datos de tarjeta. Número de pedido único y legible. | CU-17 |
| RN-P10 | Tras checkout exitoso: pedido creado con snapshots, stock descontado, carrito vaciado y pedido visible en historial. | CU-17, CU-18 |
| RN-P11 | Historial y detalle de pedidos muestran solo pedidos del dueño (filtrado por `user_id`), ordenados del más reciente al más antiguo y con totales guardados en el snapshot. | CU-18, CU-19 |
| RN-P12 | El estado mostrado al cliente es el más reciente; el detalle incluye historial de estados y la dirección usada en la compra. | CU-19 |

---

## 8. Administración y auditoría (CU-20 a CU-23, CU-25)

| ID | Regla | Fuente |
|---|---|---|
| RN-D01 | Solo usuarios con rol `admin` acceden a funciones administrativas; clientes reciben `403`. | CU-20..23, CU-25 |
| RN-D02 | Productos: precio > 0, stock entero ≥ 0, SKU único por presentación; presentaciones permitidas 30, 50 y 100 ml (según CU-20). | CU-20 |
| RN-D03 | No se eliminan físicamente productos/marcas/categorías con historial o referencias asociadas; se desactivan. Registros inactivos no aparecen al público pero sí en panel. | CU-20, CU-25 |
| RN-D04 | Cambios de catálogo no alteran snapshots de pedidos existentes. | CU-20 |
| RN-D05 | Marcas y categorías: nombre y slug únicos; categorías planas en la beta; género y familia olfativa son atributos fijos del producto. Conflictos de unicidad → `409`. | CU-25 |
| RN-D06 | Gestión administrativa de pedidos: consulta global paginada y filtrable (solo lectura en listado); cambios de estado solo por transiciones permitidas `paid → preparing → shipped → delivered`, sin retroceder ni saltar, con control de concurrencia (`409` en conflicto). | CU-21, CU-22 |
| RN-D07 | No se modifican ítems, precios ni dirección de un pedido existente desde administración. Cancelación fuera del alcance de la beta. | CU-22 |
| RN-D08 | Auditoría append-only: cada acción administrativa relevante genera un evento inmutable (actor, acción, entidad, id, resumen, fecha, IP, user-agent). Cada servicio es dueño de su auditoría; la agregación/consulta es a nivel aplicación/gateway. | CU-23, architecture.md |
| RN-D09 | Si no se puede registrar la auditoría de una acción que lo exige, la acción se revierte (`503`) para no dejar cambios sin trazabilidad. | CU-23 |
| RN-D10 | La auditoría no almacena contraseñas, tokens ni datos de tarjeta; su consulta está restringida a `admin`. | CU-23, security.md |

---

## 9. Trazabilidad rápida

| Módulo | Casos de uso | ADR/contratos clave |
|---|---|---|
| Autenticación y sesiones | CU-01..04 | ADR-0003, 0009, 0010, 0011, `security.openapi.yaml` |
| Cuenta | CU-05, CU-06, CU-24 | ADR-0009, 0011, `security.openapi.yaml` |
| Catálogo | CU-07..10 | ADR-0006, `gateway.openapi.yaml` (catalog pendiente) |
| Carrito | CU-11..15 | ADR-0006, 0007 |
| Direcciones, checkout, pedidos | CU-16..19 | ADR-0006, 0007 |
| Administración y auditoría | CU-20..23, CU-25 | ADR-0006, architecture.md |

---

## 10. Mantenimiento

- Actualizar este documento cuando cambien reglas en CU, ADR o contratos.
- Marcar explícitamente las reglas afectadas por decisiones abiertas (actualmente ADR-0004 y ADR-0005).
- Revisar consistencia con `beta-criteria.md` y contratos OpenAPI antes de cerrar una fase.
