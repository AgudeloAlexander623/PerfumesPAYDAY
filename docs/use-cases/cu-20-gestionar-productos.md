# CU-20 — Gestionar productos

| Campo | Valor |
|---|---|
| Módulo | Administración |
| Actores | Administrador (principal), catalog-service (sistema) |
| Prioridad | Must |
| Diagrama | [`08-administracion`](../diagrams/08-administracion.svg) |

## Objetivo

Permitir que el administrador cree, edite, desactive y actualice el stock de productos y sus presentaciones.

## Precondiciones

- El usuario tiene una sesión activa con rol `admin` confirmado por el servidor.

## Disparador

El administrador abre **Productos** en el panel administrativo.

## Flujo principal

1. El frontend solicita la lista de productos, incluidos los inactivos.
2. El gateway valida el token y el rol, y enruta a `catalog-service`.
3. `catalog-service` devuelve los productos con marca, categoría y presentaciones.
4. El administrador elige crear, editar, desactivar o actualizar stock.
5. El frontend valida los campos obligatorios.
6. `catalog-service` valida reglas de negocio y guarda los cambios en `catalog_db`.
7. Registra la acción en la auditoría (CU-23).
8. Devuelve el producto actualizado y el frontend refresca la lista.

## Subflujos

### S1 — Crear producto

1. El administrador ingresa nombre, marca, categoría, género, familia olfativa, descripción, notas e imagen.
2. Agrega una o más presentaciones con precio, stock y SKU.
3. `catalog-service` valida que el SKU sea único y que precio y stock sean válidos.
4. Guarda el producto en estado `active`.

### S2 — Editar producto

1. El administrador modifica datos del producto o de una presentación.
2. `catalog-service` valida y guarda los cambios.
3. Los pedidos anteriores conservan su copia y no se alteran.

### S3 — Desactivar o reactivar

1. El administrador cambia el estado del producto.
2. Un producto inactivo deja de aparecer en el catálogo público, pero sigue visible en el panel.
3. No se elimina físicamente para no romper referencias históricas.

### S4 — Actualizar stock

1. El administrador ajusta el stock de una presentación.
2. `catalog-service` valida que el valor sea un entero mayor o igual a cero.
3. Registra el cambio en la auditoría.

## Flujos alternativos

### A1 — Usuario sin rol admin

- **Cuándo ocurre:** un cliente intenta acceder a las rutas de administración.
- **Respuesta del sistema:** responde `403` y no muestra el panel.

### A2 — Datos inválidos

- **Cuándo ocurre:** falta un campo, el precio es negativo o el stock no es entero.
- **Respuesta del sistema:** responde `400` o `422` con los campos a corregir.

### A3 — SKU duplicado

- **Cuándo ocurre:** ya existe una presentación con ese SKU.
- **Respuesta del sistema:** responde `409` y no guarda el cambio.

### A4 — Producto con pedidos asociados

- **Cuándo ocurre:** se intenta eliminar un producto que ya fue vendido.
- **Respuesta del sistema:** no permite eliminarlo; solo desactivarlo.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `catalog-service` no responde.
- **Respuesta del sistema:** responde `503` y conserva el formulario para reintentar.

## Postcondiciones

- El catálogo refleja los cambios para los usuarios.
- Cada cambio administrativo queda auditado.
- Los pedidos existentes no se modifican.

## Reglas de negocio

- El rol se valida en el servidor, no solo en la interfaz.
- El precio debe ser mayor que cero y el stock mayor o igual a cero.
- El SKU es único por presentación.
- No se eliminan productos con historial de pedidos; se desactivan.
- Un producto inactivo no se muestra al público.
- Las presentaciones permitidas son 30, 50 y 100 ml.
- Los cambios de catálogo no alteran los snapshots de pedidos.

## Datos y servicios involucrados

- **Servicio:** `catalog-service`.
- **Base de datos:** `catalog_db`.
- **Entidades:** `products`, `product_variants`, `brands`, `categories`.

## Seguridad

- Autorización por rol `admin` en el gateway y en el servicio.
- Validación de todos los campos en el servidor.
- Auditoría de cada creación, edición, desactivación y cambio de stock.
- Límite de peticiones y protección contra cargas masivas.
- Las imágenes se referencian por URL validada; no se suben archivos ejecutables.

## Criterios de aceptación

- [ ] Solo un administrador accede al panel de productos.
- [ ] Se puede crear un producto con varias presentaciones.
- [ ] El SKU duplicado devuelve `409`.
- [ ] Un producto con pedidos no se puede eliminar, solo desactivar.
- [ ] El stock no admite valores negativos.
- [ ] Cada cambio queda registrado en la auditoría.
- [ ] Los pedidos anteriores no cambian.
