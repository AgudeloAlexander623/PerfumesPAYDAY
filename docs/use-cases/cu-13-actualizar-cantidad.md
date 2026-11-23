# CU-13 — Actualizar cantidad

| Campo | Valor |
|---|---|
| Módulo | Carrito |
| Actores | Cliente y Visitante (principal), order-service y catalog-service (sistema) |
| Prioridad | Must |
| Diagrama | [`05-carrito-usuario`](../diagrams/05-carrito-usuario.svg) |

## Objetivo

Cambiar la cantidad de un producto del carrito respetando el stock y el máximo permitido.

## Precondiciones

- El ítem existe en el carrito del usuario.
- La nueva cantidad es un entero positivo.

## Disparador

El usuario modifica la cantidad con los botones `+` / `-` o escribe un número.

## Flujo principal

1. El usuario cambia la cantidad.
2. **Si no tiene sesión:** el frontend valida contra el stock conocido y actualiza el `localStorage`.
3. **Si tiene sesión:** envía la nueva cantidad al gateway.
4. El gateway enruta a `order-service` y toma el `user_id` del token.
5. `order-service` verifica que el ítem pertenezca al carrito de ese usuario.
6. Revalida el stock con `catalog-service`.
7. Actualiza la cantidad y devuelve el carrito con los totales recalculados.
8. El frontend actualiza la fila y el total.

## Flujos alternativos

### A1 — Cantidad mayor al stock

- **Cuándo ocurre:** la cantidad pedida supera el stock disponible.
- **Respuesta del sistema:** responde `409` con el máximo disponible y no aplica el cambio.

### A2 — Cantidad cero

- **Cuándo ocurre:** el usuario baja la cantidad a cero.
- **Respuesta del sistema:** se interpreta como eliminación y se ejecuta CU-14.

### A3 — Ítem de otro usuario

- **Cuándo ocurre:** el identificador del ítem no pertenece al carrito del token.
- **Respuesta del sistema:** responde `404` sin confirmar que el ítem existe.

### A4 — Presentación inactiva

- **Cuándo ocurre:** el producto fue desactivado.
- **Respuesta del sistema:** responde `409` y sugiere eliminar el ítem.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `order-service` o `catalog-service` no responden.
- **Respuesta del sistema:** responde `503` y conserva la cantidad anterior.

## Postcondiciones

- La cantidad queda actualizada y los totales se recalculan.
- En A2 el ítem se elimina del carrito.

## Reglas de negocio

- La cantidad es un entero entre 1 y el menor valor entre stock y máximo por ítem.
- El servidor nunca confía en el precio enviado por el cliente.
- La actualización es por ítem, no por producto genérico.
- El carrito de invitado se valida con el stock mostrado más recientemente.

## Datos y servicios involucrados

- **Servicios:** `order-service`, `catalog-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `carts`, `cart_items`.

## Seguridad

- Se verifica la pertenencia del ítem al carrito del `user_id` del token.
- Se responde `404` en lugar de `403` para no revelar recursos ajenos.
- Se valida el tipo y rango de la cantidad en el servidor.

## Criterios de aceptación

- [ ] Cambiar la cantidad actualiza el subtotal y el total.
- [ ] No se puede superar el stock disponible.
- [ ] Cantidad cero elimina el ítem.
- [ ] Un ítem ajeno devuelve `404`.
- [ ] Un producto inactivo no permite actualizar la cantidad.
