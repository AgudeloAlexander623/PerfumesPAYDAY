# CU-25 — Gestionar marcas y categorías

| Campo | Valor |
|---|---|
| Módulo | Administración |
| Actores | Administrador (principal), catalog-service (sistema) |
| Prioridad | Should |
| Diagrama | [`08-administracion`](../diagrams/08-administracion.svg) |

## Objetivo

Mantener las marcas y categorías que usan los productos y los filtros del catálogo.

## Precondiciones

- El usuario tiene rol `admin` confirmado por el servidor.

## Disparador

El administrador abre **Marcas** o **Categorías** en el panel.

## Flujo principal

1. El frontend solicita la lista al gateway.
2. El gateway valida el rol y enruta a `catalog-service`.
3. `catalog-service` devuelve las marcas o categorías con su estado.
4. El administrador crea, edita o desactiva un registro.
5. `catalog-service` valida nombre y slug únicos, y guarda en `catalog_db`.
6. Registra la acción en la auditoría (CU-23).
7. Devuelve el registro actualizado.

## Flujos alternativos

### A1 — Nombre o slug duplicado

- **Cuándo ocurre:** ya existe una marca o categoría con ese nombre o slug.
- **Respuesta del sistema:** responde `409` y no guarda el cambio.

### A2 — Registro en uso

- **Cuándo ocurre:** se intenta eliminar una marca o categoría con productos asociados.
- **Respuesta del sistema:** no permite eliminarla; solo desactivarla.

### A3 — Datos inválidos

- **Cuándo ocurre:** el nombre está vacío o el slug tiene caracteres no permitidos.
- **Respuesta del sistema:** responde `400` o `422`.

### A4 — Usuario sin rol admin

- **Cuándo ocurre:** un cliente intenta acceder.
- **Respuesta del sistema:** responde `403`.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `catalog-service` no responde.
- **Respuesta del sistema:** responde `503` y conserva el formulario.

## Postcondiciones

- Las marcas y categorías quedan disponibles para asignarlas a productos y filtros.
- Cada cambio queda auditado.

## Reglas de negocio

- No se eliminan marcas ni categorías con productos asociados; se desactivan.
- El nombre y el slug son únicos.
- Las categorías son planas en la beta; no hay subcategorías.
- El género y la familia olfativa son valores fijos del producto, no categorías.
- Un registro inactivo no aparece en los filtros públicos, pero sigue visible en el panel.

## Datos y servicios involucrados

- **Servicio:** `catalog-service`.
- **Base de datos:** `catalog_db`.
- **Entidades:** `brands`, `categories`, `products`.

## Seguridad

- Autorización por rol `admin` en el gateway y en el servicio.
- Validación de nombre y slug en el servidor.
- Auditoría de cada cambio.
- No se permite eliminar registros referenciados.

## Criterios de aceptación

- [ ] Solo un administrador gestiona marcas y categorías.
- [ ] El nombre y el slug no se repiten.
- [ ] Una marca o categoría en uso no se elimina, solo se desactiva.
- [ ] Los cambios se reflejan en el catálogo y los filtros.
- [ ] Cada cambio queda en la auditoría.
- [ ] Un cliente recibe `403`.
