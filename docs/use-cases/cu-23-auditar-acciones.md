# CU-23 — Auditar acciones administrativas

| Campo | Valor |
|---|---|
| Módulo | Administración |
| Actores | Sistema (registro), Administrador (consulta) |
| Prioridad | Should |
| Diagrama | [`08-administracion`](../diagrams/08-administracion.svg) |

## Objetivo

Registrar de forma inmutable las acciones administrativas y permitir consultarlas para saber quién cambió qué y cuándo.

## Precondiciones

- **Registro:** se ejecutó una acción administrativa en `catalog-service` u `order-service`.
- **Consulta:** el usuario tiene rol `admin`.

## Disparador

- **Registro:** creación, edición, desactivación o cambio de stock de un producto; cambio de estado de un pedido; gestión de marcas o categorías.
- **Consulta:** el administrador abre **Auditoría** en el panel.

## Flujo principal — Registro

1. El servicio que ejecuta la acción valida y guarda el cambio.
2. En la misma transacción escribe un evento de auditoría.
3. El evento incluye actor, acción, entidad, identificador, resumen del cambio, fecha, IP y agente del navegador.
4. El evento queda en la tabla `audit_events` de la base de datos del propio servicio.

## Flujo principal — Consulta

1. El administrador abre **Auditoría**.
2. El gateway consulta en paralelo a `catalog-service` y `order-service`.
3. Cada servicio devuelve sus eventos filtrados por fecha, actor, entidad o acción.
4. El frontend combina los resultados y los ordena por fecha descendente.
5. El administrador revisa el detalle de cada evento.

## Flujos alternativos

### A1 — Usuario sin rol admin

- **Cuándo ocurre:** un cliente intenta consultar la auditoría.
- **Respuesta del sistema:** responde `403`.

### A2 — Sin eventos

- **Cuándo ocurre:** los filtros no coinciden con ningún registro.
- **Respuesta del sistema:** muestra un estado vacío y permite limpiar los filtros.

### A3 — Un servicio no responde

- **Cuándo ocurre:** `catalog-service` u `order-service` falla durante la consulta.
- **Respuesta del sistema:** muestra los eventos del servicio disponible e informa que los resultados son parciales.

### A4 — Falla al escribir la auditoría

- **Cuándo ocurre:** no se puede guardar el evento.
- **Respuesta del sistema:** la acción administrativa se revierte y se responde `503`, para no dejar cambios sin trazabilidad.

## Postcondiciones

- Cada acción administrativa tiene al menos un evento asociado.
- Los eventos no se pueden modificar ni eliminar.

## Reglas de negocio

- La auditoría es **append-only**: solo se agregan registros.
- Cada servicio es dueño de su propia auditoría; no se hacen joins entre bases de datos.
- El frontend o el gateway combinan los resultados, no la base de datos.
- No se guardan contraseñas, tokens ni datos de tarjeta.
- Los eventos se conservan durante el periodo definido por el proyecto.
- El registro y la acción ocurren en la misma transacción cuando es posible.

## Datos y servicios involucrados

- **Servicios:** `catalog-service`, `order-service`.
- **Bases de datos:** `catalog_db`, `orders_db`.
- **Entidad:** `audit_events` con `id`, `actor_id`, `action`, `entity`, `entity_id`, `summary`, `ip`, `user_agent`, `created_at`.

## Seguridad

- Solo un administrador puede consultar la auditoría.
- El usuario de base de datos de la aplicación no tiene permisos de `UPDATE` ni `DELETE` sobre `audit_events`.
- Se minimizan los datos personales guardados.
- La consulta también se registra como evento de acceso.
- La inmutabilidad protege la trazabilidad ante errores o abuso.

## Criterios de aceptación

- [ ] Cada acción administrativa genera un evento.
- [ ] Los eventos no se pueden editar ni eliminar desde la aplicación.
- [ ] La consulta muestra fecha, actor, acción y entidad.
- [ ] Los filtros por fecha, actor, entidad y acción funcionan.
- [ ] Si un servicio falla, se muestran resultados parciales con aviso.
- [ ] Un cliente recibe `403`.
- [ ] La auditoría no contiene contraseñas ni tokens.
