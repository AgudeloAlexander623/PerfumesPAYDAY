# ADR-0005 — Comunicación interna `orders` → `catalog`

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-10 |
| Decisores | Equipo |
| Relacionados | CU-11, CU-12, CU-17, [`architecture.md`](../architecture.md) §5 |

## Contexto

`order-service` necesita consultar a `catalog-service` para:

- Revalidar que una presentación existe, está activa y tiene stock (CU-11).
- Obtener precio y stock actuales al ver el carrito (CU-12).
- Revalidar precio y stock al crear el pedido (CU-17).
- Descontar stock durante el checkout (CU-17).

El gateway es el único servicio público, pero no está definido si las llamadas internas pasan por él o van directo por la red interna.

## Decisión

**Pendiente de aprobación.** Se proponen dos opciones.

### Opción A — Red interna directa

`order-service` llama a `catalog-service` por su nombre de servicio en la red de Docker o del proveedor.

| Ventajas | Desventajas |
|---|---|
| Menos latencia y menos saltos | Requiere red interna y resolución de nombres |
| El gateway no se convierte en cuello de botella | Hay que definir autenticación entre servicios |
| Separa tráfico externo de tráfico interno | Requiere timeouts, reintentos y manejo de fallos |

### Opción B — A través del gateway

`order-service` llama al gateway y este enruta a `catalog-service`.

| Ventajas | Desventajas |
|---|---|
| Un solo punto de entrada y de validación | El gateway se vuelve crítico para el negocio interno |
| Menos configuración de red | Agrega latencia y acopla el tráfico interno al público |
| Reutiliza el enrutamiento existente | Complica la autenticación servicio-a-servicio |

## Recomendación

**Opción A**, con estas condiciones:

- `catalog-service` no se expone a internet; solo es accesible desde la red interna.
- Las llamadas usan timeout y un número limitado de reintentos.
- Las operaciones de escritura (descontar stock) no se reintentan sin idempotencia.
- Se define un mecanismo de autenticación entre servicios: encabezado secreto compartido para la beta o mTLS si el tiempo alcanza.
- Los errores de `catalog` se traducen a `503` o `409` según el caso, sin filtrar detalles internos.

## Consecuencias

- Hay que documentar la red interna y los nombres de servicio en `deployment.md`.
- `order-service` necesita un cliente HTTP con timeout y manejo de errores.
- El checkout debe ser transaccional en `orders_db` y compensar si falla el descuento de stock.
- La disponibilidad de `catalog` afecta el carrito y el checkout; se debe informar con `503`.
- La auditoría de cada servicio sigue siendo local.

## Pendientes

- Aprobar la opción.
- Definir autenticación entre servicios.
- Definir timeouts, reintentos y compensación.
- Confirmar el nombre de servicio y el puerto interno de `catalog`.
- Documentar el flujo en `architecture.md` y `deployment.md`.

## Referencias

- [CU-11 — Agregar al carrito](../use-cases/cu-11-agregar-al-carrito.md)
- [CU-12 — Ver carrito](../use-cases/cu-12-ver-carrito.md)
- [CU-17 — Checkout simulado](../use-cases/cu-17-checkout-simulado.md)
- [`Backend/docs/PLAN.md`](../../Backend/docs/PLAN.md) §7
