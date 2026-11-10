# Backend

Documentación específica de esta carpeta. La visión del producto, la arquitectura global y los casos de uso están en el [README raíz](../../README.md) y en [`docs/`](../../docs/); este documento no los repite.

## 1. Alcance

El Backend agrupa los tres servicios Node.js + TypeScript que atienden la API:

- `gateway`: punto único de entrada.
- `catalog-service`: marcas, categorías, productos, presentaciones, precios y stock.
- `order-service`: carrito, direcciones, checkout, pedidos y auditoría.

`security-service` **no** vive en esta carpeta. Está en [`security/`](../../security/docs/README.md), se escribe en Python + FastAPI y es el único que emite tokens. El backend solo consume y valida esos tokens.

**Estado:** fase de planeación. No hay código de aplicación, endpoints implementados ni base de datos creada. Solo existen la estructura, la documentación, el workspace npm y las dependencias base.

## 2. Servicios

| Servicio | Responsabilidad | Base de datos | Casos de uso | Documentación |
|---|---|---|---|---|
| Gateway | Enrutar `/api/v1`, validar JWT, CORS, rate limit y trazabilidad | Ninguna | Transversal | [`gateway`](../services/gateway/docs/README.md) |
| Catalog | Catálogo, marcas, categorías, presentaciones, precios y stock | `catalog_db` | CU-07 a CU-10, CU-20, CU-25 | [`catalog`](../services/catalog/docs/README.md) |
| Orders | Carrito, direcciones, checkout, pedidos y auditoría | `orders_db` | CU-11 a CU-19, CU-21 a CU-23 | [`orders`](../services/orders/docs/README.md) |

Reglas que no cambian:

- Solo el gateway es público.
- Cada servicio es dueño de su base de datos; no hay tablas ni joins compartidos.
- `order-service` consulta a `catalog-service` para revalidar precio y stock; no lee `catalog_db` directamente.
- El `user_id` sale del token, nunca del cuerpo ni de la URL.

## 3. Stack y decisiones

| Elemento | Valor actual | Estado |
|---|---|---|
| Runtime | Node.js 22 | Confirmado |
| Lenguaje | TypeScript 7 | Instalado |
| Workspace | npm workspaces | Confirmado |
| Framework HTTP | Fastify 5 | Confirmado e instalado |
| ORM | Prisma 7 | Confirmado |
| Driver PostgreSQL | `@prisma/adapter-pg` + `pg` | Instalado |
| Validación | Zod 4 | Instalado; adopción pendiente de confirmación |
| JWT | `jose` para validar RS256 | Instalado |
| Pruebas | Vitest 5 | Instalado |
| Base de datos | PostgreSQL | Confirmado |
| Contenedores | Docker + Docker Compose | Pendiente de implementación |
| Contratos | OpenAPI por servicio | Pendiente |

Fastify se instaló en cada servicio. El gateway además usa CORS, Helmet, rate limit y proxy; catálogo y pedidos solo llevan Helmet porque no son públicos. No se instalan dependencias del frontend ni del servicio de seguridad en esta carpeta.

## 4. Estructura

```text
Backend/
├── package.json              # Workspace y dependencias base
├── package-lock.json         # Versiones bloqueadas
├── tsconfig.base.json        # Configuración TypeScript compartida
├── docs/
│   ├── README.md             # Este documento
│   └── PLAN.md               # Planeación, decisiones y pendientes
└── services/
    ├── gateway/
    │   ├── package.json
    │   ├── docs/README.md
    │   ├── src/              # Vacío
    │   └── tests/            # Vacío
    ├── catalog/
    │   ├── package.json
    │   ├── docs/README.md
    │   ├── src/              # Vacío
    │   └── tests/            # Vacío
    └── orders/
        ├── package.json
        ├── docs/README.md
        ├── src/              # Vacío
        └── tests/            # Vacío
```

## 5. Dependencias

`package.json` y `package-lock.json` son la fuente de verdad de versiones. Resumen:

| Grupo | Paquetes | Para qué |
|---|---|---|
| Runtime compartido | `@prisma/client`, `@prisma/adapter-pg`, `pg`, `zod`, `jose` | Persistencia, validación y validación de JWT |
| Gateway | `fastify`, `@fastify/cors`, `@fastify/helmet`, `@fastify/rate-limit`, `@fastify/http-proxy` | Entrada, seguridad, límite de peticiones y enrutamiento |
| Catálogo y pedidos | `fastify`, `@fastify/helmet` | API interna y cabeceras de seguridad |
| Desarrollo | `typescript`, `tsx`, `vitest`, `@vitest/coverage-v8`, `prisma`, `@types/node`, `@types/pg` | Compilación, ejecución, pruebas y migraciones |
| Workspaces | `gateway`, `catalog`, `orders` | Separar los tres servicios sin duplicar herramientas |

El cliente de Prisma se genera cuando exista el esquema de cada servicio. Mientras no haya `schema.prisma` ni `prisma generate`, `@prisma/client` no es importable.

Pendiente de instalar:

- Utilidades de prueba de integración, si hacen falta.
- Almacén externo para rate limit si se despliega más de una instancia del gateway.

Comandos disponibles desde `Backend/`:

```bash
npm install          # Instala el workspace
npm test             # Ejecuta Vitest (hoy no hay pruebas)
npm run test:watch   # Vitest en modo interactivo
```

Todavía no existe un comando para iniciar la aplicación porque no hay código de aplicación.

## 6. Estado y próximos pasos

Hecho:

- Estructura de los tres servicios.
- Workspace npm con dependencias base.
- Fastify y sus plugins instalados por servicio.
- Configuración TypeScript compartida.
- Documentación del backend y de cada servicio.

Pendiente:

1. Registrar las decisiones en ADR.
2. Definir los contratos OpenAPI de los casos `Must`.
3. Diseñar los esquemas Prisma de `catalog_db` y `orders_db`.
4. Configurar Docker, variables de entorno y CI.
5. **Solo con autorización explícita**, escribir el esqueleto de los servicios.

El detalle, las alternativas y los riesgos están en [`PLAN.md`](PLAN.md).

## 7. Documentación relacionada

| Documento | Qué contiene |
|---|---|
| [README raíz](../../README.md) | Producto, alcance, equipo, cronograma y reglas generales |
| [Casos de uso](../../docs/use-cases/README.md) | Comportamiento funcional y prioridades |
| [Diagramas](../../docs/diagrams/README.md) | Arquitectura y flujos |
| [Seguridad](../../security/docs/README.md) | Servicio de autenticación y controles |
| [`PLAN.md`](PLAN.md) | Planeación específica del backend |
| `docs/api/` | Contratos OpenAPI (pendientes) |
| `docs/adr/` | Decisiones de arquitectura (pendientes) |
