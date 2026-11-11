# Contratos de API

Documento de convenciones y contratos de la API pública de **PerfumesPAYDAY**. El gateway es el único punto de entrada; los servicios internos implementan los contratos que aquí se describen.

> **Estado:** borrador. El contrato del gateway existe a nivel de superficie; los contratos detallados de `security`, `catalog` y `orders` están pendientes y dependen de [ADR-0004](../adr/0004-propiedad-datos.md) y [ADR-0006](../adr/0006-errores-paginacion-idempotencia.md).

---

## 1. Archivos

| Archivo | Servicio | Estado |
|---|---|---|
| [`gateway.openapi.yaml`](gateway.openapi.yaml) | Gateway | Borrador |
| `security.openapi.yaml` | `security-service` | Pendiente |
| `catalog.openapi.yaml` | `catalog-service` | Pendiente |
| `orders.openapi.yaml` | `order-service` | Pendiente |

La fuente de verdad de cada contrato es el archivo OpenAPI del servicio. El gateway solo documenta la superficie pública y el enrutamiento.

---

## 2. Convenciones generales

| Tema | Convención |
|---|---|
| Base path | `/api/v1` |
| Formato | JSON, UTF-8 |
| Fechas | ISO 8601 en UTC |
| Identificadores | UUID |
| Moneda | COP (peso colombiano) |
| Nombres de rutas | Sustantivos en plural y kebab-case |
| Nombres de campos | `camelCase` |
| Autenticación | `Authorization: Bearer <access token>` |
| Refresh token | Cookie `httpOnly`, `Secure`, `SameSite` |
| Versión | `/api/v1`; un cambio incompatible crea `/api/v2` |

---

## 3. Autenticación

- Los endpoints públicos no requieren token: catálogo, búsqueda, detalle y autenticación.
- Los endpoints protegidos requieren un access token JWT válido.
- El refresh token no se envía en el cuerpo ni en la URL; viaja en cookie.
- El `user_id` y el rol salen del token; nunca del cuerpo ni de la URL.
- Las rutas de administración requieren rol `admin` validado en gateway y servicio.

**Decisión abierta:** la entrega de la clave pública está en [ADR-0003](../adr/0003-jwt-rs256.md).

---

## 4. Errores

Todas las respuestas de error usan el envelope de [ADR-0006](../adr/0006-errores-paginacion-idempotencia.md):

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos enviados no son válidos.",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "El correo no tiene un formato válido."
      }
    ],
    "requestId": "6f1c2a9e-3b7d-4c1a-9e2f-8a4b5c6d7e8f"
  }
}
```

Códigos HTTP:

| Código | Uso |
|---|---|
| `400` | Petición mal formada o parámetros inválidos. |
| `401` | Token ausente, inválido o expirado. |
| `403` | Autenticado sin permiso. |
| `404` | Recurso inexistente o ajeno. |
| `409` | Conflicto de negocio o de idempotencia. |
| `422` | Regla de negocio incumplida. |
| `429` | Rate limit. |
| `500` | Error interno. |
| `503` | Dependencia no disponible. |

---

## 5. Paginación

Listados de catálogo, historial, administración y auditoría usan:

| Parámetro | Tipo | Por defecto | Máximo |
|---|---|---|---|
| `page` | entero ≥ 1 | `1` | — |
| `pageSize` | entero ≥ 1 | `20` | `100` |

Respuesta:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 57,
    "totalPages": 3
  }
}
```

---

## 6. Idempotencia

- Header `Idempotency-Key` obligatorio en `POST /api/v1/orders` y `POST /api/v1/cart/merge`.
- Valor UUID v4 generado por el frontend.
- Misma clave + mismo cuerpo devuelve la respuesta guardada.
- Misma clave + cuerpo distinto devuelve `409` con código `IDEMPOTENCY_CONFLICT`.
- Retención propuesta: 24 horas.

---

## 7. Mapa de rutas

| Prefijo | Servicio | Casos de uso | Autenticación |
|---|---|---|---|
| `/health` | Gateway | — | Pública |
| `/api/v1/auth/*` | `security-service` | CU-01 a CU-04 | Pública / cookie |
| `/api/v1/users/me` | `security-service` | CU-05, CU-06, CU-24 | Bearer |
| `/api/v1/products*` | `catalog-service` | CU-07 a CU-09 | Pública |
| `/api/v1/brands`, `/api/v1/categories` | `catalog-service` | CU-07, CU-08, CU-25 | Pública (lectura) |
| `/api/v1/cart*` | `order-service` | CU-11 a CU-15 | Bearer |
| `/api/v1/addresses*` | `order-service` | CU-16 | Bearer |
| `/api/v1/orders*` | `order-service` | CU-17 a CU-19 | Bearer |
| `/api/v1/admin/products*` | `catalog-service` | CU-20 | Bearer + `admin` |
| `/api/v1/admin/brands*`, `/api/v1/admin/categories*` | `catalog-service` | CU-25 | Bearer + `admin` |
| `/api/v1/admin/orders*` | `order-service` | CU-21, CU-22 | Bearer + `admin` |
| `/api/v1/admin/audit` | `catalog` + `orders` | CU-23 | Bearer + `admin` |

> **CU-10** (página de mayoristas) es una página estática del frontend. No genera endpoints en la beta.

---

## 8. Contratos por servicio

### `security-service`

- Registro, login, refresh y logout.
- Perfil propio y cambio de contraseña.
- Emisión y rotación de tokens.
- No gestiona catálogo, carrito, direcciones ni pedidos.

### `catalog-service`

- Catálogo público paginado y filtrable.
- Detalle de producto con presentaciones, precio y stock.
- Administración de productos, marcas, categorías y stock.
- Revalidación de precio y stock para `order-service`.
- Auditoría de acciones de catálogo.

### `order-service`

- Carrito autenticado y fusión del carrito de invitado.
- Direcciones de envío.
- Checkout idempotente y snapshots.
- Historial y detalle de pedidos.
- Administración de pedidos y auditoría.

### Gateway

- `/health`.
- Enrutamiento de `/api/v1/*`.
- Validación de JWT y rol.
- CORS, Helmet, rate limit y `requestId`.
- Agregación de auditoría de `catalog` y `orders` (CU-23).

---

## 9. Flujo de trabajo de un contrato

1. El caso de uso define el comportamiento y los criterios de aceptación.
2. El ADR correspondiente define las decisiones transversales.
3. Se escribe o actualiza el archivo OpenAPI del servicio.
4. Se revisa el contrato con frontend, backend y seguridad.
5. Se implementa el endpoint y se agregan pruebas de contrato.
6. El gateway se actualiza si cambia la superficie pública.
7. La documentación se actualiza en el mismo pull request.

Reglas:

- No se implementa un endpoint sin contrato.
- No se cambia un contrato sin actualizar el caso de uso y las pruebas.
- Los errores, la paginación y la idempotencia siguen [ADR-0006](../adr/0006-errores-paginacion-idempotencia.md).
- Los contratos se validan con una herramienta OpenAPI (Redocly CLI, Swagger Editor o similar) antes de integrarlos.

---

## 10. Validación

Comandos sugeridos cuando exista la herramienta instalada:

```bash
npx @redocly/cli lint docs/api/gateway.openapi.yaml
```

No se instala ninguna dependencia en esta fase; el comando es una referencia para cuando se autorice.

---

## 11. Referencias

- [Arquitectura](../architecture.md)
- [Seguridad](../security.md)
- [ADR](../adr/README.md)
- [Casos de uso](../use-cases/README.md)
- [Diagramas](../diagrams/README.md)

---

**Última actualización:** 2026-11-10
**Estado:** convenciones redactadas; contratos de servicio pendientes.
