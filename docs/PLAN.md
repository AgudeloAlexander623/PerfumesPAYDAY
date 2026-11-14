# Backend — plan de planeación

> Documento de trabajo. No autoriza código de aplicación ni reemplaza los contratos OpenAPI.
> El alcance general está en el [README raíz](../README.md); el comportamiento funcional, en los [casos de uso](use-cases/README.md).

## 1. Objetivo

Decidir cómo se construirá el backend antes de escribir código: framework, contratos, esquemas, dependencias y orden de trabajo. La meta es que cada servicio tenga límites claros y que ninguna decisión se tome por accidente.

## 2. Restricciones

- Beta académica de 3 semanas y 4 personas.
- Microservicios obligatorios; una base de datos por servicio.
- Gateway como único servicio público; JWT RS256 emitido por `security-service`.
- PostgreSQL, Docker y TypeScript.
- Sin pagos reales, DIAN, Kafka, Kubernetes real ni app móvil en esta fase.
- No se escribe código de aplicación sin autorización explícita.

## 3. Lluvia de ideas: framework HTTP

`Vite` se incluyó en la comparación porque apareció como opción, pero **no es un framework de backend**: es una herramienta de build para el frontend. Por eso queda descartado para la API.

| Criterio | Fastify | NestJS | Vite |
|---|---|---|---|
| Rol | Framework HTTP para Node | Framework completo para Node | Build tool de frontend |
| Curva | Baja | Media/alta | No aplica al backend |
| Estructura | Libre y ligera | Módulos, DI y decoradores | No aplica |
| Rendimiento | Muy alto | Alto | No aplica |
| Validación | Zod o esquemas propios | DTOs y `class-validator` | No aplica |
| Pruebas | Vitest + inyección manual | Jest + `TestingModule` | No aplica |
| Instalación | `npm i fastify` + plugins | `nest new` + módulos | `npm create vite` |
| Documentación | Breve y orientada a plugins | Extensa y muy estructurada | Enfocada al frontend |
| Escalabilidad | Buena con servicios pequeños | Buena para equipos grandes | No aplica |
| Integración | Plugins oficiales | Ecosistema propio | React/Vue |
| Ideal para | Beta corta y microservicios | Equipos grandes con reglas | SPA React/Vue |
| Riesgo | Menos convenciones | Más peso y tiempo | No sirve como API |
| Veredicto | **Seleccionado** | Alternativa válida | **Descartado** |

**Decisión:** Fastify. Tres servicios pequeños, un equipo de 4 personas y 3 semanas favorecen una base ligera, rápida de arrancar y fácil de probar. NestJS queda descartado para esta beta y Vite no aplica al backend.

## 4. Ideas evaluadas

| Tema | Opciones | Idea inicial | Estado |
|---|---|---|---|
| Framework | Fastify / NestJS / Vite | Fastify | Confirmado |
| ORM | Prisma / Drizzle | Prisma | Confirmado |
| Dependencias | npm workspaces / package por servicio | npm workspaces | Confirmado |
| Validación | Zod / manual | Zod | Propuesto |
| Autenticación | JWT RS256 | Validar en gateway y servicios | Definido por arquitectura |
| API | REST/JSON `/api/v1` | OpenAPI por servicio | Pendiente |
| Errores | Envelope JSON uniforme | Definir en ADR | Pendiente |
| Paginación | Offset / cursor | Offset para catálogo beta | Pendiente |
| Idempotencia | Header `Idempotency-Key` | Carrito y checkout | Definido en CU-15 y CU-17 |
| Logs | JSON estructurado | Sin datos personales | Pendiente |
| Bases de datos | Una por servicio | Sin joins entre bases | Confirmado |
| Mensajería | REST / broker | REST, sin Kafka | Definido por alcance |

## 5. Fases de trabajo

| Fase | Objetivo | Entregables | Depende de |
|---|---|---|---|
| F0 | Base documental y técnica | README, este plan, workspace, dependencias base | — |
| F1 | Decisiones y contratos | ADR de framework, API, auth y datos; OpenAPI de los `Must` | F0 |
| F2 | Esqueleto técnico | Dockerfiles, configuración, healthchecks, arnés de pruebas | F1 + autorización |
| F3 | Catálogo | Esquema Prisma de `catalog_db`, endpoints, seeds y pruebas | F2 |
| F4 | Pedidos | Esquema Prisma de `orders_db`, carrito, direcciones, checkout y pruebas | F3 |
| F5 | Integración de seguridad | Validación de JWT, roles y manejo uniforme de errores | F2 |
| F6 | Cierre | Endurecimiento, pruebas de flujo, documentación y demo | F3, F4 y F5 |

La autorización para código aplica desde F2. F0 y F1 son documentación y decisiones.

Estado actual: F0 y F2 están completas. De F1 solo está aceptado ADR-0008; faltan ADR-0003, ADR-0004, ADR-0005 y ADR-0006. F5 está avanzada: la validación JWT RS256, los claims, los guards de rol y el proxy del gateway con CORS y rate limit ya funcionan; falta el emisor real en `security-service` y la agregación de auditoría.

La secuencia detallada, el orden de dependencias y las puertas de salida de cada fase están en [`ROADMAP.md`](ROADMAP.md).

## 6. Dependencias

Criterio: instalar solo lo que se use y evitar paquetes que dupliquen funciones.

| Grupo | Paquetes | Estado | Destino |
|---|---|---|---|
| Base | `typescript`, `tsx`, `vitest`, `@vitest/coverage-v8`, `prisma` | Instalado | `Backend/package.json` |
| Tipos | `@types/node`, `@types/pg` | Instalado | `Backend/package.json` |
| Datos | `@prisma/client`, `@prisma/adapter-pg`, `pg` | Instalado | `Backend/package.json` |
| Validación | `zod` | Instalado; adopción por confirmar | `Backend/package.json` |
| JWT | `jose` | Instalado | `Backend/package.json` |
| Gateway | `fastify`, `@fastify/cors`, `@fastify/helmet`, `@fastify/rate-limit`, `@fastify/http-proxy` | Instalado | Paquete del gateway |
| Catálogo y pedidos | `fastify`, `@fastify/helmet` | Instalado | Paquete de cada servicio |
| Pruebas de integración | `supertest` u equivalente | Pendiente | Paquete del servicio |
| Frontend y seguridad | React, FastAPI, etc. | Fuera de esta carpeta | Otros componentes |

Cuando se elija el framework se instalarán sus plugins en cada servicio, no en la raíz, salvo que sean herramientas compartidas. `prisma` se queda en la raíz porque es una herramienta de desarrollo; los esquemas y clientes se generan por servicio.

## 7. Riesgos y preguntas abiertas

- **Fastify:** ya está elegido; falta validar la configuración de plugins y el proxy del gateway.
- **Rate limit:** el almacén en memoria sirve para una instancia; si se escala, hará falta Redis u otro almacén externo.
- **Prisma 7:** requiere `@prisma/adapter-pg` y `pg`; el cliente aún no está generado y hay que confirmar la configuración de conexión y la ruta de generación.
- **Workspaces:** npm puede hoistar dependencias y ocultar una que falte en un servicio. Verificar con `npm ls` al agregar paquetes.
- **Contratos:** faltan el formato de error, la paginación y los códigos de respuesta uniformes.
- **JWT:** falta decidir si la clave pública se pasa por variable de entorno o por archivo montado.
- **Comunicación interna:** falta confirmar si `order-service` llama a `catalog-service` por red interna directa o a través del gateway. La arquitectura sugiere red interna directa, sin exponer el servicio.
- **Auditoría e idempotencia:** falta definir retención, limpieza y responsables.
- **Entornos:** Docker y `.env.example` ya existen; falta CI.
- **Código:** el esqueleto fue autorizado; cada etapa de negocio requiere autorización explícita.

## 8. Próximos pasos

1. Crear los ADR de framework, formato de errores, autenticación y propiedad de datos.
2. Convertir los casos `Must` en contratos OpenAPI.
3. Diseñar los esquemas Prisma por servicio.
4. Instalar las utilidades de prueba de integración cuando existan endpoints.
5. Pedir autorización y recién entonces crear el esqueleto de los servicios.

## 9. Registro de decisiones

| Fecha | Decisión | Estado |
|---|---|---|
| 2026-11-10 | Usar Prisma con `@prisma/adapter-pg` y `pg` | Confirmado |
| 2026-11-10 | Organizar el backend con npm workspaces | Confirmado |
| 2026-11-10 | Instalar base TypeScript, Vitest, Zod, `jose` y Prisma | Hecho |
| 2026-11-10 | Usar Fastify 5 con plugins por servicio | Confirmado e instalado |
| 2026-11-10 | ADR-0008: ESM, project references y paquete `@perfumespayday/shared` | Aceptado |
| 2026-11-10 | Esqueleto del backend con `/health`, Docker y pruebas | Hecho |
| 2026-11-10 | Contratos OpenAPI y ADR restantes | Pendiente |
