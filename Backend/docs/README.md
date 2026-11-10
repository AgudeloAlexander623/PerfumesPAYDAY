# Backend

Documentación específica de esta carpeta. La visión del producto, la arquitectura global y los casos de uso están en el [README raíz](../../README.md) y en [`docs/`](../../docs/); este documento no los repite.

## 1. Alcance

El Backend agrupa los tres servicios Node.js + TypeScript que atienden la API:

- `gateway`: punto único de entrada.
- `catalog-service`: marcas, categorías, productos, presentaciones, precios y stock.
- `order-service`: carrito, direcciones, checkout, pedidos y auditoría.

`security-service` **no** vive en esta carpeta. Está en [`security/`](../../security/docs/README.md), se escribe en Python + FastAPI y es el único que emite tokens. El backend solo consume y valida esos tokens.

**Estado:** esqueleto técnico implementado. Los tres servicios compilan, arrancan y responden `GET /health`; todavía no hay endpoints de negocio, base de datos creada ni contratos implementados.

## 2. Servicios

| Servicio | Responsabilidad | Base de datos | Casos de uso | Código |
|---|---|---|---|---|
| Gateway | Enrutar `/api/v1`, validar JWT, CORS, rate limit y trazabilidad | Ninguna | Transversal | [`services/gateway`](../services/gateway/) |
| Catalog | Catálogo, marcas, categorías, presentaciones, precios y stock | `catalog_db` | CU-07 a CU-10, CU-20, CU-25 | [`services/catalog`](../services/catalog/) |
| Orders | Carrito, direcciones, checkout, pedidos y auditoría | `orders_db` | CU-11 a CU-19, CU-21 a CU-23 | [`services/orders`](../services/orders/) |

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
| Módulos | ESM con `"type": "module"` | Aceptado en [ADR-0008](../../docs/adr/0008-modulos-typescript.md) |
| Compilación | `tsc -b` con project references | Implementado |
| Workspace | npm workspaces | Confirmado |
| Framework HTTP | Fastify 5 | Confirmado e instalado |
| Paquete compartido | `@perfumespayday/shared` | Implementado |
| ORM | Prisma 7 | Confirmado |
| Driver PostgreSQL | `@prisma/adapter-pg` + `pg` | Instalado |
| Validación | Zod 4 | Instalado y en uso para el entorno |
| JWT | `jose` para validar RS256 | Instalado; se usará en el gateway |
| Pruebas | Vitest 5 | Instalado; 7 pruebas en verde |
| Base de datos | PostgreSQL | Confirmado |
| Contenedores | Docker + Docker Compose | Implementado para el backend |
| Contratos | OpenAPI por servicio | Pendiente |

Fastify y Helmet viven en `@perfumespayday/shared` para no repetirlos en cada servicio. El gateway conserva CORS, rate limit, proxy y `jose` porque los usará en la etapa de integración. Catálogo y pedidos solo dependen del paquete compartido.

## 4. Estructura

```text
Backend/
├── package.json              # Workspace y dependencias base
├── package-lock.json         # Versiones bloqueadas
├── tsconfig.base.json        # Configuración TypeScript compartida
├── tsconfig.json             # Solución de project references
├── vitest.config.ts          # Pruebas y alias del paquete compartido
├── Dockerfile                # Imagen parametrizada por SERVICE
├── docker-compose.yml        # Gateway público; servicios internos
├── .env.example
├── .dockerignore
├── docs/
│   ├── README.md             # Este documento
│   ├── PLAN.md               # Planeación, decisiones y pendientes
│   └── ROADMAP.md            # Ruta de desarrollo por etapas
├── packages/
│   └── shared/
│       ├── package.json
│       ├── tsconfig.json
│       ├── src/              # app, env, errors y lifecycle
│       └── tests/
├── services/
│   ├── gateway/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   │       ├── config/env.ts
│   │       └── server.ts
│   ├── catalog/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   │       ├── config/env.ts
│   │       └── server.ts
│   └── orders/
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
│           ├── config/env.ts
│           └── server.ts
└── tests/
    └── services.test.ts      # Humo de los tres servicios
```

Cada servicio solo declara su configuración y su punto de entrada. La lógica transversal está una sola vez en `packages/shared`.

## 5. Dependencias

`package.json` y `package-lock.json` son la fuente de verdad de versiones. Resumen:

| Grupo | Paquetes | Para qué |
|---|---|---|
| Compartido | `@perfumespayday/shared` | Configuración, errores, salud y ciclo de vida |
| Runtime del compartido | `fastify`, `@fastify/helmet`, `zod` | Servidor, cabeceras de seguridad y validación |
| Gateway | `@fastify/cors`, `@fastify/rate-limit`, `@fastify/http-proxy`, `jose` | Entrada, límite de peticiones, proxy y JWT |
| Persistencia base | `@prisma/client`, `@prisma/adapter-pg`, `pg` | Acceso a datos de catálogo y pedidos |
| Desarrollo | `typescript`, `tsx`, `vitest`, `@vitest/coverage-v8`, `prisma`, `@types/node`, `@types/pg` | Compilación, ejecución, pruebas y migraciones |
| Workspaces | `packages/*`, `gateway`, `catalog`, `orders` | Compartir herramientas sin duplicar configuración |

El cliente de Prisma se genera cuando exista el esquema de cada servicio. Mientras no haya `schema.prisma` ni `prisma generate`, `@prisma/client` no es importable.

Pendiente de instalar:

- Utilidades de prueba de integración, si hacen falta.
- Almacén externo para rate limit si se despliega más de una instancia del gateway.

Comandos disponibles desde `Backend/`:

```bash
npm install          # Instala el workspace
npm run build        # Compila shared y los tres servicios
npm test             # Ejecuta Vitest
npm run test:watch   # Vitest en modo interactivo
npm run dev:gateway  # Gateway en el puerto 3000
npm run dev:catalog  # Catálogo en el puerto 3001
npm run dev:orders   # Pedidos en el puerto 3002
npm run clean        # Limpia los artefactos de compilación
```

Cada servicio lee `PORT`, `HOST`, `LOG_LEVEL` y `NODE_ENV`; los valores de ejemplo están en [`.env.example`](../.env.example). En producción:

```bash
npm run build
npm run start -w @perfumespayday/gateway
```

Docker levanta los tres servicios y solo publica el gateway:

```bash
docker compose up --build
```

## 6. Estado y próximos pasos

Hecho:

- Estructura de los tres servicios.
- Workspace npm con dependencias base.
- ESM y project references según [ADR-0008](../../docs/adr/0008-modulos-typescript.md).
- Paquete `@perfumespayday/shared` con configuración, errores, `/health`, `requestId`, Helmet y ciclo de vida.
- Esqueleto de `gateway`, `catalog` y `orders` que compila y arranca.
- Dockerfile parametrizado, Docker Compose y `.env.example`.
- Pruebas de humo y verificación del contenedor.

Pendiente:

1. Aceptar ADR-0003, ADR-0004, ADR-0005 y ADR-0006.
2. Definir los contratos OpenAPI de los casos `Must`.
3. Diseñar los esquemas Prisma de `catalog_db` y `orders_db`.
4. Implementar catálogo (etapa 4 del [ROADMAP](ROADMAP.md)).
5. Integrar el gateway y la seguridad (etapa 6) y configurar CI.

El detalle, las alternativas y los riesgos están en [`PLAN.md`](PLAN.md). La secuencia de trabajo, las puertas de salida y el registro de avance están en [`ROADMAP.md`](ROADMAP.md).

## 7. Documentación relacionada

| Documento | Qué contiene |
|---|---|
| [README raíz](../../README.md) | Producto, alcance, equipo, cronograma y reglas generales |
| [Casos de uso](../../docs/use-cases/README.md) | Comportamiento funcional y prioridades |
| [Diagramas](../../docs/diagrams/README.md) | Arquitectura y flujos |
| [Seguridad](../../security/docs/README.md) | Servicio de autenticación y controles |
| [`PLAN.md`](PLAN.md) | Planeación específica del backend |
| [`ROADMAP.md`](ROADMAP.md) | Ruta de desarrollo por etapas y puertas de salida |
| [`docs/api/`](../../docs/api/README.md) | Contratos OpenAPI (pendientes) |
| [`docs/adr/`](../../docs/adr/README.md) | Decisiones de arquitectura |
