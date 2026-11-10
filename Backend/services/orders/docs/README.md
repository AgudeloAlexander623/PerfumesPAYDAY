# Order Service

## Responsabilidad

Dueño del carrito autenticado, las direcciones de envío, el checkout simulado, los pedidos y la auditoría de sus operaciones. Convierte el carrito en un pedido con una copia inmutable de productos, precios y dirección.

## Límites

- Es dueño exclusivo de `orders_db`; no lee `catalog_db` directamente.
- No emite credenciales ni valida contraseñas; recibe el `user_id` desde el token.
- Revalida precio y stock contra `catalog-service` antes de crear el pedido.
- No procesa pagos reales: el pago se registra como simulado.
- No permite consultar pedidos ni direcciones de otro usuario.
- La auditoría es append-only y propia; no hace joins con otros servicios.

## Datos

Entidades previstas en los casos de uso:

- `carts`
- `cart_items`
- `addresses`
- `orders`
- `order_items`
- `order_addresses`
- `order_status_history`
- `audit_events`
- Claves de idempotencia para carrito y checkout

## Casos de uso

| Caso | Relación |
|---|---|
| CU-11 a CU-15 | Carrito: agregar, ver, actualizar, eliminar y fusionar |
| CU-16 | Gestionar direcciones |
| CU-17 | Checkout simulado e idempotente |
| CU-18 y CU-19 | Historial y detalle de pedidos |
| CU-21 y CU-22 | Consulta y estado de pedidos desde administración |
| CU-23 | Auditoría de acciones administrativas |

## Dependencias

- Node.js 22 + TypeScript 7.
- Prisma 7 con `@prisma/adapter-pg` y `pg`.
- Zod para validar entradas.
- `jose` para validar JWT y rol.
- Fastify 5.
- `@fastify/helmet` para cabeceras de seguridad.
- Cliente HTTP interno hacia `catalog-service`.

## Variables de entorno propuestas

| Variable | Uso |
|---|---|
| `PORT` | Puerto del servicio |
| `DATABASE_URL` | Conexión a `orders_db` |
| `CATALOG_SERVICE_URL` | URL interna del catálogo |
| `JWT_PUBLIC_KEY` | Clave pública para validar tokens |

## Estado

Fase de planeación. No hay esquema Prisma, código, endpoints, transacciones ni pruebas.

## Referencias

- [Backend](../../../docs/README.md)
- [Plan del backend](../../../docs/PLAN.md)
- [CU-11](../../../../docs/use-cases/cu-11-agregar-al-carrito.md)
- [CU-17](../../../../docs/use-cases/cu-17-checkout-simulado.md)
- [CU-19](../../../../docs/use-cases/cu-19-detalle-pedido.md)
- [Diagrama de checkout](../../../../docs/diagrams/06-direcciones-checkout.mmd)
