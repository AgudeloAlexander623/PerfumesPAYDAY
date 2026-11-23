# CU-12 — Ver carrito

| Campo | Valor |
|---|---|
| Módulo | Carrito |
| Actores | Cliente y Visitante (principal), order-service y catalog-service (sistema) |
| Prioridad | Must |
| Diagrama | [`05-carrito-usuario`](../diagrams/05-carrito-usuario.svg) |

## Objetivo

Mostrar los productos del carrito con su cantidad, precio actual, subtotal y total.

## Precondiciones

- Ninguna. Un carrito vacío también es un estado válido.

## Disparador

El usuario abre el carrito desde el ícono del encabezado o desde el detalle de un producto.

## Flujo principal

1. **Si no tiene sesión:** el frontend lee del `localStorage` solo `variant_id` y cantidad.
2. Consulta a `catalog-service` los datos actuales de esas presentaciones.
3. Calcula subtotales y total en el navegador solo para mostrar.
4. **Si tiene sesión:** el frontend solicita el carrito al gateway.
5. El gateway enruta a `order-service`, que toma el `user_id` del token.
6. `order-service` carga los ítems y consulta a `catalog-service` precio y stock actuales.
7. Devuelve los ítems enriquecidos y los totales calculados en el servidor.
8. El frontend muestra productos, cantidades, subtotales y total.
9. Si algún precio o stock cambió, muestra un aviso visible.

## Flujos alternativos

### A1 — Carrito vacío

- **Cuándo ocurre:** no hay ítems guardados.
- **Respuesta del sistema:** muestra un estado vacío con un enlace al catálogo.

### A2 — Producto no disponible

- **Cuándo ocurre:** una presentación fue desactivada o quedó sin stock.
- **Respuesta del sistema:** marca el ítem como no disponible, impide continuar al checkout y permite eliminarlo.

### A3 — Precio modificado

- **Cuándo ocurre:** el precio actual difiere del último visto.
- **Respuesta del sistema:** muestra el precio vigente y avisa del cambio antes de continuar.

### A4 — Servicio no disponible

- **Cuándo ocurre:** `order-service` o `catalog-service` no responden.
- **Respuesta del sistema:** responde `503` y ofrece reintentar sin perder el carrito.

## Postcondiciones

- El usuario conoce el contenido real y el total estimado de su carrito.

## Reglas de negocio

- El carrito de invitado guarda solo identificadores y cantidades, nunca precios.
- Los totales del carrito autenticado se calculan en el servidor.
- El total es informativo; el monto definitivo se calcula en el checkout.
- No se puede continuar al checkout si hay ítems inválidos.
- La moneda es el peso colombiano (COP).

## Datos y servicios involucrados

- **Servicios:** `order-service`, `catalog-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `carts`, `cart_items`.

## Seguridad

- El `user_id` se toma del token; no se acepta como parámetro.
- Un usuario solo puede leer su propio carrito.
- No se exponen datos de otros usuarios ni identificadores internos.

## Criterios de aceptación

- [ ] El carrito muestra productos, cantidades, subtotales y total.
- [ ] Un carrito vacío muestra un estado claro.
- [ ] Un ítem sin stock se marca y bloquea el checkout.
- [ ] Un cambio de precio se informa al usuario.
- [ ] Un usuario no puede ver el carrito de otro.
