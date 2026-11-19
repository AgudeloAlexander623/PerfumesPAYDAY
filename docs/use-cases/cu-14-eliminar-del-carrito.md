# CU-14 — Eliminar producto del carrito

| Campo | Valor |
|---|---|
| Módulo | Carrito |
| Actores | Cliente y Visitante (principal), order-service (sistema) |
| Prioridad | Must |
| Diagrama | [`05-carrito-usuario`](../diagrams/05-carrito-usuario.svg) |

## Objetivo

Quitar un producto del carrito de forma definitiva y recalcular los totales.

## Precondiciones

- El ítem existe en el carrito del usuario o en el carrito temporal.

## Disparador

El usuario selecciona **Eliminar** sobre un ítem.

## Flujo principal

1. El usuario confirma la eliminación.
2. **Si no tiene sesión:** el frontend elimina el ítem del `localStorage` y actualiza el contador.
3. **Si tiene sesión:** envía la solicitud al gateway.
4. El gateway enruta a `order-service` y toma el `user_id` del token.
5. `order-service` verifica que el ítem pertenezca al carrito del usuario.
6. Elimina el ítem y devuelve el carrito actualizado.
7. El frontend quita la fila y recalcula el total.

## Flujos alternativos

### A1 — El ítem ya no existe

- **Cuándo ocurre:** se eliminó en otra pestaña o en otra petición.
- **Respuesta del sistema:** responde `204` igualmente; la operación es idempotente.

### A2 — Ítem de otro usuario

- **Cuándo ocurre:** el identificador no pertenece al carrito del token.
- **Respuesta del sistema:** responde `404` sin revelar si el ítem existe.

### A3 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** responde `503` y conserva el ítem para reintentar.

## Postcondiciones

- El ítem ya no aparece en el carrito.
- Si era el último, el carrito queda vacío pero sigue existiendo.
- Los totales se recalculan.

## Reglas de negocio

- Eliminar el último ítem no borra el carrito del usuario.
- La eliminación es idempotente.
- Eliminar un ítem no afecta pedidos ya creados.
- El carrito de invitado solo se modifica en el navegador.

## Datos y servicios involucrados

- **Servicio:** `order-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `carts`, `cart_items`.

## Seguridad

- Se verifica la pertenencia del ítem al carrito del `user_id` del token.
- Se responde `404` para no filtrar información sobre ítems ajenos.
- No se acepta `user_id` desde el cuerpo ni desde la URL.

## Criterios de aceptación

- [ ] El usuario puede eliminar un ítem de su carrito.
- [ ] El total se recalcula después de eliminar.
- [ ] Eliminar dos veces el mismo ítem no genera error.
- [ ] Un ítem ajeno devuelve `404`.
- [ ] Los pedidos anteriores no se modifican.
