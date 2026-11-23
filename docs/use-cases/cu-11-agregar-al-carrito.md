# CU-11 — Agregar producto al carrito

| Campo | Valor |
|---|---|
| Módulo | Carrito |
| Actores | Cliente y Visitante (principal), order-service y catalog-service (sistema) |
| Prioridad | Must |
| Diagrama | [`05-carrito-usuario`](../diagrams/05-carrito-usuario.svg) |

## Objetivo

Agregar una presentación de perfume al carrito con una cantidad válida, respetando el stock disponible.

## Precondiciones

- El producto está activo y la presentación elegida tiene stock.
- La cantidad es un número entero mayor que cero.

## Disparador

El usuario selecciona **Agregar al carrito** desde el detalle del producto.

## Flujo principal

1. El usuario elige la presentación y la cantidad.
2. **Si no tiene sesión:** el frontend valida contra el último stock conocido, guarda `variant_id` y cantidad en `localStorage` y actualiza el contador del carrito.
3. **Si tiene sesión:** el frontend envía `variant_id` y cantidad al gateway.
4. El gateway enruta la petición a `order-service` y toma el `user_id` del token.
5. `order-service` revalida con `catalog-service` que la presentación exista, esté activa y tenga stock suficiente.
6. Si la presentación ya está en el carrito, suma las cantidades sin superar el stock ni el máximo por ítem.
7. Guarda el carrito y sus ítems en `orders_db`.
8. Devuelve el carrito actualizado con cantidades y totales.
9. El frontend actualiza el contador y muestra una confirmación breve.

## Flujos alternativos

### A1 — Stock insuficiente

- **Cuándo ocurre:** la cantidad pedida supera el stock disponible.
- **Respuesta del sistema:** responde `409` con la cantidad disponible y permite ajustarla.

### A2 — Producto inactivo o inexistente

- **Cuándo ocurre:** la presentación fue desactivada o eliminada del catálogo.
- **Respuesta del sistema:** responde `404` o `409` y no agrega el ítem.

### A3 — Cantidad inválida

- **Cuándo ocurre:** la cantidad es cero, negativa, decimal o supera el máximo permitido.
- **Respuesta del sistema:** responde `400` con el rango permitido.

### A4 — Servicio no disponible

- **Cuándo ocurre:** `catalog-service` u `order-service` no responden.
- **Respuesta del sistema:** responde `503` y no guarda un ítem sin validar.

### A5 — Carrito de invitado corrupto

- **Cuándo ocurre:** el `localStorage` tiene datos inválidos.
- **Respuesta del sistema:** el frontend descarta ese carrito y empieza uno vacío.

## Postcondiciones

- El ítem queda en el carrito del usuario o en el carrito temporal del navegador.
- El contador del carrito refleja la nueva cantidad.

## Reglas de negocio

- El carrito de invitado vive solo en el navegador; el autenticado vive en `order-service`.
- El carrito autenticado se asocia al `user_id` del token, nunca a un identificador enviado por el cliente.
- El precio no se guarda como fuente de verdad; se consulta al mostrar el carrito y se revalida en el checkout.
- La cantidad máxima por ítem es el menor valor entre el stock y el límite definido por el negocio.
- Agregar un producto repetido suma cantidades, no crea filas duplicadas.

## Datos y servicios involucrados

- **Servicios:** `order-service`, `catalog-service`.
- **Base de datos:** `orders_db` para el carrito autenticado.
- **Entidades:** `carts`, `cart_items`.
- **Datos externos:** `product_variants` de `catalog_db` (stock y estado).

## Seguridad

- El `user_id` se toma del token; se rechaza cualquier `user_id` del cuerpo.
- Se valida que la variante exista antes de guardar.
- El precio y el stock siempre vienen del servidor.
- Límite de peticiones por usuario para evitar abuso.
- Un usuario no puede escribir en el carrito de otro.

## Criterios de aceptación

- [ ] Un visitante puede agregar productos y ve el contador actualizado.
- [ ] Un cliente autenticado guarda el carrito en el servidor.
- [ ] No se puede agregar más cantidad que el stock disponible.
- [ ] Una cantidad inválida devuelve `400`.
- [ ] Un producto inactivo no se agrega.
- [ ] El carrito siempre queda asociado al usuario del token.
