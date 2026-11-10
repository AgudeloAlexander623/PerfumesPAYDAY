# Catalog Service

## Responsabilidad

Dueño del catálogo de perfumes: marcas, categorías, productos, presentaciones, precios y stock. Atiende la consulta pública y las operaciones administrativas del catálogo.

## Límites

- Es dueño exclusivo de `catalog_db`; ningún otro servicio lee sus tablas directamente.
- No gestiona usuarios, credenciales, carritos ni pedidos.
- Expone lectura pública y escritura solo para el rol `admin`.
- Registra la auditoría de sus acciones administrativas; no consulta la auditoría de otros servicios.
- Revalida precio y stock cuando `order-service` lo solicita durante el checkout.

## Datos

Entidades previstas en los casos de uso:

- `brands`
- `categories`
- `products`
- `product_variants`
- `audit_events` (acciones administrativas propias)

Los precios se expresan en COP y el stock se controla por presentación.

## Casos de uso

| Caso | Relación |
|---|---|
| CU-07 a CU-09 | Explorar, buscar, filtrar y ver detalle |
| CU-10 | Página de mayoristas (contenido, sin lógica B2B) |
| CU-20 | Gestionar productos |
| CU-25 | Gestionar marcas y categorías |

## Dependencias

- Node.js 22 + TypeScript 7.
- Prisma 7 con `@prisma/adapter-pg` y `pg`.
- Zod para validar entradas.
- `jose` para validar JWT y rol.
- Fastify 5.
- `@fastify/helmet` para cabeceras de seguridad.

## Variables de entorno propuestas

| Variable | Uso |
|---|---|
| `PORT` | Puerto del servicio |
| `DATABASE_URL` | Conexión a `catalog_db` |
| `JWT_PUBLIC_KEY` | Clave pública para validar tokens |

## Estado

Fase de planeación. No hay esquema Prisma, código, endpoints ni datos de prueba.

## Referencias

- [Backend](../../../docs/README.md)
- [Plan del backend](../../../docs/PLAN.md)
- [CU-07](../../../../docs/use-cases/cu-07-explorar-catalogo.md)
- [CU-20](../../../../docs/use-cases/cu-20-gestionar-productos.md)
- [CU-25](../../../../docs/use-cases/cu-25-gestionar-marcas-categorias.md)
- [Diagrama de catálogo](../../../../docs/diagrams/04-catalogo.mmd)
