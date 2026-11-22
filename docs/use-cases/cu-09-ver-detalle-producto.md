# CU-09 — Ver detalle de producto

| Campo | Valor |
|---|---|
| Módulo | Catálogo |
| Actores | Visitante y Cliente (principal) |
| Prioridad | Must |
| Diagrama | [`04-catalogo`](../diagrams/04-catalogo.svg) |

## Objetivo

Mostrar toda la información de un perfume y permitir elegir la presentación antes de agregarlo al carrito.

## Precondiciones

- El producto existe y está activo.

## Disparador

El usuario selecciona un producto desde el catálogo o desde un resultado de búsqueda.

## Flujo principal

1. El frontend solicita el producto por su identificador.
2. El gateway enruta la petición a `catalog-service`.
3. `catalog-service` consulta el producto, su marca, categoría y presentaciones.
4. Devuelve nombre, descripción, notas, imagen y las presentaciones de 30, 50 y 100 ml con su precio y stock.
5. El frontend muestra el detalle y preselecciona una presentación disponible.
6. El usuario cambia de presentación si lo desea.
7. El frontend actualiza precio y disponibilidad según la presentación elegida.
8. Si hay stock, el usuario puede agregar el producto al carrito (CU-11).

## Flujos alternativos

### A1 — Producto inexistente o inactivo

- **Cuándo ocurre:** el identificador no existe o el producto fue desactivado.
- **Respuesta del sistema:** responde `404`; el frontend muestra una página de producto no encontrado.

### A2 — Todas las presentaciones agotadas

- **Cuándo ocurre:** ninguna variante tiene stock.
- **Respuesta del sistema:** muestra el aviso de agotado y deshabilita el botón de agregar.

### A3 — Servicio no disponible

- **Cuándo ocurre:** `catalog-service` no responde.
- **Respuesta del sistema:** responde `503` y ofrece reintentar.

## Postcondiciones

- El usuario conoce el precio y el stock de la presentación elegida.
- No se modifica ningún dato del catálogo.

## Reglas de negocio

- Cada presentación tiene su propio precio y stock.
- Un producto inactivo no es visible para el público.
- El precio mostrado es de referencia y se revalida en el checkout.
- La presentación elegida se envía al carrito, no el producto genérico.

## Datos y servicios involucrados

- **Servicio:** `catalog-service`.
- **Base de datos:** `catalog_db`.
- **Entidades:** `products`, `product_variants`, `brands`, `categories`.

## Seguridad

- Endpoint público con límite de peticiones.
- No se exponen costos internos ni datos de auditoría.
- El identificador se valida como UUID antes de consultar.

## Criterios de aceptación

- [ ] El detalle muestra marca, descripción, notas y presentaciones.
- [ ] Al cambiar de presentación cambian precio y stock.
- [ ] Un producto inactivo devuelve `404`.
- [ ] Si no hay stock, el botón de agregar está deshabilitado.
- [ ] El detalle no expone campos internos.
