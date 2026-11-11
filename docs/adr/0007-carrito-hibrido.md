# ADR-0007 — Carrito híbrido

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-10 |
| Decisores | Equipo |
| Relacionados | CU-11 a CU-15, [`docs/use-cases/RESUMEN.md`](../use-cases/RESUMEN.md) |

## Contexto

Un visitante debe poder armar un carrito sin registrarse. Un cliente autenticado debe conservar su carrito entre dispositivos y sesiones. Guardar precios en el navegador permitiría manipularlos. El equipo necesitaba una decisión única para no duplicar lógica entre frontend y backend.

## Decisión

Se adopta un **carrito híbrido**:

- **Visitante:** el carrito vive en `localStorage` y guarda solo `variant_id` y cantidad. Nunca guarda precios.
- **Cliente autenticado:** el carrito vive en `order-service` (`orders_db`, entidades `carts` y `cart_items`) y se asocia al `user_id` del token.
- **Al iniciar sesión:** el carrito de invitado se fusiona con el carrito del usuario mediante `POST /api/v1/cart/merge`, con clave de idempotencia y topes de stock (CU-15).
- **Precios y stock:** siempre se consultan al servidor; el total del carrito es informativo y se recalcula en el checkout.
- **Cantidades:** se suman sin superar el stock ni el máximo por ítem; no se crean filas duplicadas.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| Solo `localStorage` | Simple y sin backend | No se comparte entre dispositivos ni se conserva al cambiar de navegador | Rechazado |
| Solo backend | Una sola fuente de verdad | Obliga a registrarse para agregar productos; peor experiencia | Rechazado |
| Híbrido | Permite comprar como invitado y conserva el carrito al iniciar sesión | Requiere fusión y manejo de conflictos | **Aceptado** |

## Consecuencias

- El frontend necesita lógica para el carrito local, la fusión y el manejo de conflictos.
- `order-service` necesita un endpoint de fusión idempotente.
- El carrito autenticado se conserva al cerrar sesión; el de invitado no.
- El checkout exige sesión y dirección propias.
- Los precios nunca se confían al cliente.

## Pendientes

- Definir el máximo de ítems por carrito y por ítem.
- Definir el comportamiento exacto cuando la fusión supera el stock.
- Implementar la fusión con idempotencia ([ADR-0006](0006-errores-paginacion-idempotencia.md)).

## Referencias

- [CU-11 — Agregar al carrito](../use-cases/cu-11-agregar-al-carrito.md)
- [CU-12 — Ver carrito](../use-cases/cu-12-ver-carrito.md)
- [CU-13 — Actualizar cantidad](../use-cases/cu-13-actualizar-cantidad.md)
- [CU-14 — Eliminar del carrito](../use-cases/cu-14-eliminar-del-carrito.md)
- [CU-15 — Fusionar carrito](../use-cases/cu-15-fusionar-carrito.md)
- [`docs/use-cases/RESUMEN.md`](../use-cases/RESUMEN.md)
