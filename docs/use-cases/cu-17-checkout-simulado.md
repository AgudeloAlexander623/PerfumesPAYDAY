# CU-17 — Realizar checkout simulado

| Campo | Valor |
|---|---|
| Módulo | Checkout y direcciones |
| Actores | Cliente (principal), order-service y catalog-service (sistema) |
| Prioridad | Must |
| Diagrama | [`06-direcciones-checkout`](../diagrams/06-direcciones-checkout.svg) |

## Objetivo

Convertir el carrito en un pedido con los precios y el stock vigentes, guardar una copia de los datos y registrar un pago simulado.

## Precondiciones

- El usuario tiene una sesión activa.
- El carrito tiene al menos un ítem válido.
- El usuario tiene una dirección de envío propia.
- El frontend generó una clave de idempotencia para la compra.

## Disparador

El usuario selecciona **Finalizar compra** y confirma.

## Flujo principal

1. El usuario revisa el carrito y selecciona una dirección.
2. El frontend envía `address_id` y la clave de idempotencia al gateway.
3. El gateway valida el token y enruta a `order-service`; el `user_id` sale del token.
4. `order-service` verifica la clave de idempotencia; si ya existe, devuelve el pedido creado antes.
5. Carga el carrito y la dirección, y confirma que ambos pertenecen al usuario.
6. Revalida con `catalog-service` el precio y el stock de cada presentación.
7. Si todo es válido, crea el pedido, sus ítems y la copia de la dirección dentro de una transacción.
8. Solicita a `catalog-service` descontar el stock; si falla, revierte el pedido.
9. Marca el pago como simulado y aprobado, y genera el número de pedido.
10. Vacía el carrito y devuelve la confirmación con el número de pedido.

## Flujos alternativos

### A1 — Precio modificado

- **Cuándo ocurre:** el precio actual difiere del mostrado en el carrito.
- **Respuesta del sistema:** responde `409` con el detalle, no crea el pedido y devuelve al carrito para que el usuario confirme el nuevo total.

### A2 — Stock insuficiente

- **Cuándo ocurre:** una presentación ya no tiene la cantidad pedida.
- **Respuesta del sistema:** responde `409` con la cantidad disponible y no crea el pedido.

### A3 — Carrito vacío o inválido

- **Cuándo ocurre:** no hay ítems o alguno está desactivado.
- **Respuesta del sistema:** responde `409` y pide volver al carrito.

### A4 — Dirección ajena o inexistente

- **Cuándo ocurre:** el `address_id` no pertenece al usuario.
- **Respuesta del sistema:** responde `404` sin revelar si existe.

### A5 — Reintento de la misma compra

- **Cuándo ocurre:** se repite la petición por un fallo de red.
- **Respuesta del sistema:** devuelve el pedido ya creado; no genera un segundo pedido.

### A6 — Falla al descontar stock

- **Cuándo ocurre:** `catalog-service` no puede actualizar el inventario.
- **Respuesta del sistema:** revierte la creación del pedido y responde `503`; no deja estados parciales.

### A7 — Servicio no disponible

- **Cuándo ocurre:** `order-service` o `catalog-service` no responden.
- **Respuesta del sistema:** responde `503` y conserva el carrito intacto.

## Postcondiciones

- Existe un pedido con copia de productos, precios y dirección del momento de la compra.
- El pago queda registrado como simulado y aprobado.
- El stock de las presentaciones compradas se descuenta.
- El carrito queda vacío.
- El pedido aparece en el historial (CU-18).

## Reglas de negocio

- El servidor recalcula subtotales y total; nunca confía en montos del cliente.
- Los datos del pedido son una copia inmutable: cambios posteriores de precio o dirección no lo alteran.
- La clave de idempotencia es obligatoria y evita pedidos duplicados.
- El pago es simulado; no se solicita ni se almacena ningún dato de tarjeta.
- La moneda es el peso colombiano (COP).
- El envío es simulado; si tiene costo, se suma en el servidor.
- El número de pedido es legible para el usuario y único.

## Datos y servicios involucrados

- **Servicios:** `order-service`, `catalog-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `orders`, `order_items`, `order_addresses`, `order_status_history`.
- **Datos externos:** `product_variants` de `catalog_db` (precio y stock).

## Seguridad

- El `user_id` se toma del token.
- Se verifica que la dirección y el carrito pertenezcan al usuario.
- La idempotencia evita duplicados por reintentos o doble clic.
- La transacción y la compensación evitan pedidos a medias.
- No se manejan datos de tarjetas reales.
- La operación se registra para auditoría (CU-23).

## Criterios de aceptación

- [ ] Un cliente con carrito y dirección puede crear un pedido.
- [ ] El pedido guarda copia de productos, precios y dirección.
- [ ] El total se calcula en el servidor.
- [ ] Un cambio de precio o stock bloquea la compra con `409`.
- [ ] Reintentar la compra no duplica el pedido.
- [ ] Una falla de stock no deja pedidos parciales.
- [ ] El carrito queda vacío tras la compra.
- [ ] El pedido aparece en el historial.
