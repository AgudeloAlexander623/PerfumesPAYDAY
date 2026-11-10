# Gateway

## Responsabilidad

Punto único de entrada de la API. Recibe las peticiones del frontend, valida la sesión, aplica controles generales y las dirige al servicio correcto.

## Límites

- Es el único servicio público; los demás viven en la red interna.
- Valida el JWT RS256 emitido por `security-service` y el rol cuando la ruta lo exige.
- Aplica CORS, rate limit, request ID y logs sin datos personales.
- Enruta bajo el prefijo `/api/v1`.
- No tiene base de datos, no calcula precios, no modifica stock y no contiene reglas de negocio.

## Enrutamiento

Los prefijos exactos y los endpoints se definirán en los contratos OpenAPI. Por ahora solo se conoce el dominio que atiende cada servicio:

| Dominio | Destino | Referencia |
|---|---|---|
| Autenticación y sesiones | `security-service` | [Seguridad](../../../../security/docs/README.md) |
| Catálogo, marcas y categorías | `catalog-service` | [Catalog](../../catalog/docs/README.md) |
| Carrito, direcciones, checkout y pedidos | `order-service` | [Orders](../../orders/docs/README.md) |

## Dependencias

- Node.js 22 + TypeScript 7.
- Fastify 5.
- `@fastify/cors` para orígenes permitidos.
- `@fastify/helmet` para cabeceras de seguridad.
- `@fastify/rate-limit` para limitar peticiones.
- `@fastify/http-proxy` para enrutar a los servicios internos.
- `jose` para validar JWT (dependencia compartida del workspace).

## Variables de entorno propuestas

Nombres de trabajo, sujetos a confirmación en un ADR:

| Variable | Uso |
|---|---|
| `PORT` | Puerto del gateway |
| `SECURITY_SERVICE_URL` | URL interna del servicio de seguridad |
| `CATALOG_SERVICE_URL` | URL interna del catálogo |
| `ORDERS_SERVICE_URL` | URL interna de pedidos |
| `CORS_ORIGINS` | Orígenes permitidos |
| `JWT_PUBLIC_KEY` | Clave pública para validar tokens |

## Estado

Fase de planeación. No hay código, rutas implementadas ni configuración de entorno.

## Referencias

- [Backend](../../../docs/README.md)
- [Plan del backend](../../../docs/PLAN.md)
- [Casos de uso](../../../../docs/use-cases/README.md)
- [Diagramas](../../../../docs/diagrams/README.md)
