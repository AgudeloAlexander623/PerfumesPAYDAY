# CU-18 — Consultar historial de pedidos

| Campo | Valor |
|---|---|
| Módulo | Pedidos |
| Actores | Cliente (principal), order-service (sistema) |
| Prioridad | Must |
| Diagrama | [`07-historial-pedidos`](../diagrams/07-historial-pedidos.svg) |

## Objetivo

Mostrar al cliente la lista de sus pedidos con fecha, estado y total, del más reciente al más antiguo.

## Precondiciones

- El usuario tiene una sesión activa.

## Disparador

El usuario selecciona **Mis pedidos**.

## Flujo principal

1. El frontend solicita la primera página del historial al gateway.
2. El gateway valida el token y enruta a `order-service`.
3. `order-service` consulta `orders_db` filtrando por el `user_id` del token.
4. Ordena los pedidos del más reciente al más antiguo.
5. Devuelve número de pedido, fecha, estado, cantidad de ítems y total.
6. El frontend muestra la lista con etiquetas de estado legibles.
7. El usuario puede cambiar de página o abrir un pedido (CU-19).

## Flujos alternativos

### A1 — Sin pedidos

- **Cuándo ocurre:** el usuario nunca ha comprado.
- **Respuesta del sistema:** muestra un estado vacío con un enlace al catálogo.

### A2 — Sesión expirada

- **Cuándo ocurre:** el access token ya no es válido.
- **Respuesta del sistema:** se ejecuta CU-03; si falla, se redirige al login.

### A3 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** responde `503` y ofrece reintentar.

## Postcondiciones

- El usuario visualiza únicamente sus pedidos.

## Reglas de negocio

- El historial se filtra siempre por el `user_id` del token.
- El total mostrado proviene de la copia guardada en el pedido, no del precio actual.
- La paginación tiene un tamaño por defecto y un máximo.
- Los estados se muestran en español.
- No se muestran notas internas de administración.

## Datos y servicios involucrados

- **Servicio:** `order-service`.
- **Base de datos:** `orders_db`.
- **Entidad:** `orders`.

## Seguridad

- El `user_id` se toma del token; nunca se acepta como parámetro.
- La consulta filtra por propietario en la base de datos.
- No se revela la existencia de pedidos de otros usuarios.
- Se limita el tamaño de página para evitar consultas masivas.

## Criterios de aceptación

- [ ] El cliente ve solo sus pedidos.
- [ ] Cada pedido muestra fecha, estado y total.
- [ ] El orden es del más reciente al más antiguo.
- [ ] Sin pedidos se muestra un estado vacío.
- [ ] La paginación funciona.
- [ ] El total coincide con el guardado al momento de la compra.
