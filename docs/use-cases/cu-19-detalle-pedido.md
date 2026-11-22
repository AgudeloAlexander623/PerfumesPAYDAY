# CU-19 — Ver detalle de un pedido

| Campo | Valor |
|---|---|
| Módulo | Pedidos |
| Actores | Cliente (principal), order-service (sistema) |
| Prioridad | Must |
| Diagrama | [`07-historial-pedidos`](../diagrams/07-historial-pedidos.svg) |

## Objetivo

Mostrar el detalle completo de un pedido propio usando los datos guardados en el momento de la compra.

## Precondiciones

- El usuario tiene una sesión activa.
- El pedido existe y pertenece al usuario.

## Disparador

El usuario selecciona un pedido desde el historial.

## Flujo principal

1. El frontend solicita el pedido por su identificador.
2. El gateway valida el token y enruta a `order-service`.
3. `order-service` busca el pedido por `id` **y** por el `user_id` del token en la misma consulta.
4. Devuelve número, fecha, estado, ítems, dirección de envío, subtotal, envío y total.
5. Devuelve también el historial de estados del pedido.
6. El frontend muestra el detalle y la línea de tiempo del estado.

## Flujos alternativos

### A1 — Pedido inexistente

- **Cuándo ocurre:** el identificador no existe.
- **Respuesta del sistema:** responde `404` con una página de no encontrado.

### A2 — Pedido de otro usuario

- **Cuándo ocurre:** el pedido existe, pero pertenece a otra cuenta.
- **Respuesta del sistema:** responde `404`, igual que en A1, para no revelar que el pedido existe.

### A3 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** responde `503` y ofrece reintentar.

## Postcondiciones

- El usuario visualiza el pedido sin modificar ningún dato.

## Reglas de negocio

- Los datos del pedido son inmutables: reflejan el momento de la compra.
- Un pedido solo puede verlo su dueño o un administrador desde el panel (CU-22).
- El detalle incluye la dirección tal como se usó, aunque luego se edite o elimine.
- El estado mostrado es el más reciente del historial.

## Datos y servicios involucrados

- **Servicio:** `order-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `orders`, `order_items`, `order_addresses`, `order_status_history`.

## Seguridad

- La consulta filtra por `id` y `user_id` al mismo tiempo.
- No se filtra en memoria después de traer el pedido; así se evita una fuga por error.
- Se responde `404` en lugar de `403` para no confirmar la existencia de pedidos ajenos.
- No se exponen notas internas ni datos del administrador.

## Criterios de aceptación

- [ ] El dueño ve el detalle completo de su pedido.
- [ ] El detalle usa los datos guardados al comprar.
- [ ] Un pedido ajeno devuelve `404`.
- [ ] Se muestra el historial de estados.
- [ ] La dirección del pedido no cambia si se edita la dirección actual.
