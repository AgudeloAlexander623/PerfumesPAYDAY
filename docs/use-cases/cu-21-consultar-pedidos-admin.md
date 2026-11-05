# CU-21 — Consultar pedidos (administrador)

| Campo | Valor |
|---|---|
| Módulo | Administración |
| Actores | Administrador (principal), order-service (sistema) |
| Prioridad | Must |
| Diagrama | [`08-administracion`](../diagrams/08-administracion.svg) |

## Objetivo

Permitir que el administrador consulte y filtre todos los pedidos de la tienda.

## Precondiciones

- El usuario tiene una sesión activa con rol `admin` confirmado por el servidor.

## Disparador

El administrador abre **Pedidos** en el panel administrativo.

## Flujo principal

1. El frontend solicita la lista de pedidos al gateway.
2. El gateway valida el token y el rol, y enruta a `order-service`.
3. `order-service` consulta todos los pedidos, sin filtrar por usuario.
4. Devuelve número, fecha, estado, total y datos mínimos del cliente.
5. El frontend muestra una tabla paginada.
6. El administrador puede filtrar por estado, rango de fechas, número de pedido o correo del cliente.
7. Al seleccionar un pedido, se abre su detalle administrativo (CU-22).

## Flujos alternativos

### A1 — Usuario sin rol admin

- **Cuándo ocurre:** un cliente intenta acceder.
- **Respuesta del sistema:** responde `403` y no muestra datos.

### A2 — Sin resultados

- **Cuándo ocurre:** los filtros no coinciden con ningún pedido.
- **Respuesta del sistema:** muestra un estado vacío y permite limpiar los filtros.

### A3 — Filtro inválido

- **Cuándo ocurre:** el rango de fechas está invertido o el estado no existe.
- **Respuesta del sistema:** responde `400` con el filtro a corregir.

### A4 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** responde `503` y ofrece reintentar.

## Postcondiciones

- El administrador visualiza los pedidos según los filtros aplicados.

## Reglas de negocio

- Solo el rol `admin` puede consultar pedidos de todos los usuarios.
- La consulta es de solo lectura; los cambios de estado se hacen en CU-22.
- Se muestran únicamente los datos del cliente necesarios para gestionar el pedido.
- La paginación es obligatoria.
- Los filtros se combinan con **Y**.

## Datos y servicios involucrados

- **Servicio:** `order-service`.
- **Base de datos:** `orders_db`.
- **Entidades:** `orders`, `users` (solo datos mínimos del cliente).

## Seguridad

- Autorización por rol `admin` en el gateway y en el servicio.
- Minimización de datos personales: nombre y correo, no dirección completa en la lista.
- No se muestran datos de pago reales porque el pago es simulado.
- Se registra el acceso administrativo para auditoría.

## Criterios de aceptación

- [ ] Solo un administrador puede ver todos los pedidos.
- [ ] La tabla muestra número, fecha, estado, total y cliente.
- [ ] Los filtros por estado, fecha, número y correo funcionan.
- [ ] Un filtro inválido devuelve `400`.
- [ ] La lista está paginada.
- [ ] Un cliente recibe `403` si intenta acceder.
