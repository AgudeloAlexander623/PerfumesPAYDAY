# CU-15 — Fusionar carrito al iniciar sesión

| Campo | Valor |
|---|---|
| Módulo | Carrito |
| Actores | Cliente (principal), order-service y catalog-service (sistema) |
| Prioridad | Must |
| Diagrama | [`05-carrito-usuario`](../diagrams/05-carrito-usuario.svg) |

## Objetivo

Unir el carrito temporal del navegador con el carrito del usuario autenticado, sin perder productos ni superar el stock.

## Precondiciones

- El usuario acaba de iniciar sesión correctamente (CU-02).
- Puede existir un carrito de invitado en `localStorage`.

## Disparador

El frontend detecta un carrito de invitado después del login o en la primera petición autenticada.

## Flujo principal

1. El frontend lee el carrito de invitado (`variant_id` y cantidad).
2. Genera una clave de idempotencia para ese intento de fusión.
3. Envía los ítems al gateway.
4. El gateway enruta a `order-service` y toma el `user_id` del token.
5. `order-service` carga el carrito del usuario; si no existe, lo crea.
6. Valida cada presentación con `catalog-service`: que esté activa y con stock.
7. Si la presentación ya está en el carrito, suma cantidades con tope; si no, la agrega.
8. Guarda el carrito fusionado y devuelve el resultado, incluyendo los ítems omitidos y el motivo.
9. El frontend reemplaza el carrito de invitado por el carrito del servidor y borra el `localStorage`.

## Flujos alternativos

### A1 — Algunos ítems no están disponibles

- **Cuándo ocurre:** una presentación fue desactivada o quedó sin stock.
- **Respuesta del sistema:** omite esos ítems, los informa en la respuesta y continúa con el resto.

### A2 — El stock no alcanza para la suma

- **Cuándo ocurre:** la cantidad del invitado más la del servidor supera el stock.
- **Respuesta del sistema:** ajusta al máximo disponible e informa el cambio.

### A3 — Reintento de la misma fusión

- **Cuándo ocurre:** se repite la petición por un fallo de red.
- **Respuesta del sistema:** la clave de idempotencia evita duplicar cantidades y devuelve el mismo resultado.

### A4 — No hay carrito de invitado

- **Cuándo ocurre:** el usuario inicia sesión sin haber agregado productos.
- **Respuesta del sistema:** no hace nada y devuelve el carrito del servidor.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** conserva el carrito de invitado y reintenta más tarde; no lo borra.

## Postcondiciones

- Existe un solo carrito asociado al usuario.
- El carrito de invitado se borra solo si la fusión fue exitosa.
- Los ítems omitidos se informan al usuario.

## Reglas de negocio

- Después de la fusión, el carrito del servidor es la fuente de verdad.
- Nunca se fusiona con el carrito de otro usuario.
- Las cantidades se suman con tope de stock y máximo por ítem.
- La operación es idempotente.
- Si un ítem no está disponible, se omite; no se guarda como inválido.

## Datos y servicios involucrados

- **Servicios:** `order-service`, `catalog-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `carts`, `cart_items`.

## Seguridad

- El `user_id` se toma del token.
- Se valida el tamaño del payload y el tipo de cada ítem.
- La clave de idempotencia evita duplicados por reintentos.
- No se confía en precios enviados por el navegador.
- El carrito de invitado nunca se asocia a una cuenta sin autenticación.

## Criterios de aceptación

- [ ] Al iniciar sesión, el carrito de invitado se fusiona con el del usuario.
- [ ] Los productos repetidos suman cantidades sin duplicar filas.
- [ ] Las cantidades se ajustan al stock disponible.
- [ ] Los ítems no disponibles se informan y se omiten.
- [ ] Reintentar la fusión no duplica cantidades.
- [ ] Si la fusión falla, el carrito de invitado se conserva.
