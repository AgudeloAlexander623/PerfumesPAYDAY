# ADR-0006 — Errores, paginación e idempotencia

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-10 |
| Decisores | Equipo |
| Relacionados | [`api/README.md`](../api/README.md), CU-07, CU-11, CU-15, CU-17, CU-18, CU-21 |

## Contexto

Los casos de uso definen respuestas `400`, `401`, `403`, `404`, `409`, `422`, `429` y `503`, pero no existe un formato uniforme de error. Tampoco están definidos la paginación ni el mecanismo de idempotencia del carrito y el checkout. Sin esto, cada servicio inventaría su propio formato y el frontend tendría que adaptarse a cada uno.

## Decisión propuesta

### 1. Envelope de error

Todas las respuestas de error usan el mismo cuerpo:

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

Reglas:

- `code` es un identificador estable en mayúsculas y snake_case; el frontend puede usarlo para decidir.
- `message` es un mensaje genérico en español, apto para el usuario.
- `details` es opcional y solo aparece en errores de validación.
- `requestId` permite correlacionar con los logs.
- Nunca se incluyen trazas, SQL, nombres de tablas, tokens ni datos personales.

### 2. Códigos HTTP

| Código | Uso |
|---|---|
| `400` | Petición mal formada o parámetros inválidos. |
| `401` | Falta el token, es inválido o expiró. |
| `403` | Autenticado, pero sin permiso (por ejemplo, cliente en ruta admin). |
| `404` | Recurso inexistente o ajeno; no se confirma su existencia. |
| `409` | Conflicto: correo duplicado, SKU duplicado, stock insuficiente, precio cambiado, estado desactualizado o conflicto de idempotencia. |
| `422` | Datos bien formados pero que incumplen una regla de negocio (por ejemplo, contraseña débil). |
| `429` | Límite de peticiones superado. |
| `500` | Error interno no previsto. |
| `503` | Dependencia no disponible (base de datos, `catalog`, `security`). |

> Los casos de uso que dicen `400` o `422` se interpretan así: `400` para formato/tipo y `422` para regla de negocio. Cada contrato OpenAPI concreta cuál aplica.

### 3. Paginación

Listados de catálogo, historial, pedidos administrativos y auditoría usan paginación por offset:

- Query: `page` (entero, base 1, por defecto `1`) y `pageSize` (entero, por defecto `20`, máximo `100`).
- Respuesta:

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

- Una página fuera de rango devuelve `400` o la última página disponible; el contrato de cada servicio debe elegir una y documentarla.
- El tamaño máximo evita respuestas enormes y consultas masivas.

### 4. Idempotencia

- Header obligatorio `Idempotency-Key` en `POST /api/v1/orders` y `POST /api/v1/cart/merge`.
- Valor: UUID v4 generado por el frontend.
- Alcance: usuario + ruta + clave.
- Se guarda la clave, un hash del cuerpo, el estado y el cuerpo de la respuesta.
- Repetir la misma clave con el mismo cuerpo devuelve la respuesta guardada, sin repetir la operación.
- Repetir la misma clave con un cuerpo distinto devuelve `409` con código `IDEMPOTENCY_CONFLICT`.
- Retención propuesta: 24 horas; se puede ajustar.
- Si la clave falta en una operación que la exige, se responde `400` con código `IDEMPOTENCY_KEY_REQUIRED`.

### 5. Versionado

- Todas las rutas públicas usan `/api/v1`.
- Un cambio incompatible crea `/api/v2`; no se rompe `v1` dentro de la beta.
- Los contratos OpenAPI se versionan junto con la ruta.

## Alternativas consideradas

| Tema | Alternativa | Veredicto |
|---|---|---|
| Errores | Formato libre por servicio | Rechazado: el frontend tendría que adaptarse a cada uno. |
| Errores | Problem Details (RFC 9457) | Válido, pero más pesado para la beta; se puede migrar después. |
| Paginación | Cursor | Mejor para volúmenes grandes, innecesario para 25–30 productos. |
| Idempotencia | Solo en checkout | Insuficiente: la fusión de carrito también puede repetirse. |
| Idempotencia | Sin header, deduplicar por contenido | Frágil y propenso a falsos positivos. |

## Consecuencias

- Todos los servicios deben implementar el mismo envelope.
- El frontend puede manejar errores de forma uniforme.
- El checkout y la fusión de carrito necesitan una tabla o almacén de idempotencia.
- Los contratos OpenAPI deben declarar `Idempotency-Key` y el esquema de error.
- Los logs deben incluir `requestId` para correlacionar.

## Pendientes

- Aprobar el formato.
- Definir los códigos de error concretos por servicio.
- Definir la retención de idempotencia.
- Definir si la paginación fuera de rango devuelve `400` o la última página.
- Implementar el middleware de errores en gateway y servicios.

## Referencias

- [`api/README.md`](../api/README.md)
- [CU-07 — Explorar catálogo](../use-cases/cu-07-explorar-catalogo.md)
- [CU-11 — Agregar al carrito](../use-cases/cu-11-agregar-al-carrito.md)
- [CU-15 — Fusionar carrito](../use-cases/cu-15-fusionar-carrito.md)
- [CU-17 — Checkout simulado](../use-cases/cu-17-checkout-simulado.md)
- [CU-18 — Historial de pedidos](../use-cases/cu-18-historial-pedidos.md)
- [CU-21 — Consultar pedidos (admin)](../use-cases/cu-21-consultar-pedidos-admin.md)
