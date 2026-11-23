# CU-22 — Revisar estado de un pedido

| Campo | Valor |
|---|---|
| Módulo | Administración |
| Actores | Administrador (principal), order-service (sistema) |
| Prioridad | Should |
| Diagrama | [`08-administracion`](../diagrams/08-administracion.svg) |

## Objetivo

Permitir que el administrador consulte el detalle de un pedido y avance su estado por las transiciones permitidas.

## Precondiciones

- El usuario tiene rol `admin` confirmado por el servidor.
- El pedido existe.

## Disparador

El administrador selecciona un pedido desde la lista de CU-21.

## Flujo principal

1. El frontend solicita el detalle administrativo del pedido.
2. El gateway valida el rol y enruta a `order-service`.
3. `order-service` devuelve cliente, ítems, dirección, totales e historial de estados.
4. El administrador elige el siguiente estado permitido.
5. El frontend envía el nuevo estado junto con el estado actual como control de concurrencia.
6. `order-service` valida que la transición sea permitida y que el estado no haya cambiado.
7. Actualiza el pedido y agrega una entrada al historial de estados.
8. Registra la acción en la auditoría (CU-23).
9. Devuelve el pedido actualizado.

## Flujos alternativos

### A1 — Transición no permitida

- **Cuándo ocurre:** se intenta retroceder o saltar un estado.
- **Respuesta del sistema:** responde `409` con las transiciones válidas.

### A2 — Cambio concurrente

- **Cuándo ocurre:** otro administrador actualizó el pedido primero.
- **Respuesta del sistema:** responde `409` y pide recargar el pedido antes de reintentar.

### A3 — Usuario sin rol admin

- **Cuándo ocurre:** un cliente intenta acceder.
- **Respuesta del sistema:** responde `403`.

### A4 — Pedido inexistente

- **Cuándo ocurre:** el identificador no existe.
- **Respuesta del sistema:** responde `404`.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** responde `503` y no cambia el estado.

## Postcondiciones

- El pedido queda en el nuevo estado y el cambio se agrega al historial.
- El cliente ve el estado actualizado en su historial.
- La acción queda auditada.

## Reglas de negocio

- Las transiciones permitidas son: `paid` → `preparing` → `shipped` → `delivered`.
- No se permite retroceder ni saltar estados.
- La cancelación de pedidos está fuera del alcance de la beta.
- No se pueden modificar ítems, precios ni dirección de un pedido existente.
- Cada cambio de estado se audita con el actor y la fecha.

## Datos y servicios involucrados

- **Servicio:** `order-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `orders`, `order_status_history`, `audit_events`.

## Seguridad

- Autorización por rol `admin` en el gateway y en el servicio.
- Control de concurrencia para evitar sobrescribir cambios.
- Auditoría obligatoria de cada transición.
- No se exponen notas internas al cliente.

## Criterios de aceptación

- [ ] El administrador ve el detalle completo del pedido.
- [ ] Solo se permiten las transiciones definidas.
- [ ] Un cambio concurrente devuelve `409`.
- [ ] Cada cambio queda en el historial y en la auditoría.
- [ ] El cliente ve el nuevo estado.
- [ ] Un cliente recibe `403` si intenta cambiar el estado.
