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
| Autenticación | JWT RS256 | Validar en gateway y servicios | Confirmado (ADR-0003, ADR-0010) |
| Sesiones | Refresh opaco + rotación | Cookie `httpOnly` y revocación | Confirmado (ADR-0009) |
| Contraseñas | Argon2id | Longitud mínima de 12 | Confirmado (ADR-0011) |
| API | REST/JSON `/api/v1` | OpenAPI por servicio | Pendiente (`security.openapi.yaml`) |
| Errores | Envelope JSON uniforme | Definir en ADR | Confirmado (ADR-0006) |
| Paginación | Offset / cursor | Offset para catálogo beta | Confirmado (ADR-0006) |
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

Estado actual: F0 y F2 están completas. En F1 están aceptados ADR-0003, ADR-0006, ADR-0008, ADR-0009, ADR-0010 y ADR-0011; faltan ADR-0004 (propiedad de datos de catálogo/pedidos) y ADR-0005 (comunicación interna). F5 está avanzada: la validación JWT RS256, los claims, los guards de rol, el proxy del gateway con CORS y rate limit y el emisor `security-service` ya funcionan. Falta el ciclo de sesiones (registro, login, refresh y logout), la base `security_db`, el contrato `security.openapi.yaml` y la agregación de auditoría.

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
- **Contratos:** el envelope, la paginación y la idempotencia ya están aceptados (ADR-0006); falta escribir `security.openapi.yaml` y los contratos de catálogo/pedidos.
- **JWT:** resuelto en ADR-0003: JWKS como mecanismo principal y PEM por entorno como respaldo. Falta implementar la rotación con múltiples claves.
- **Sesiones:** resuelto en ADR-0009 y ADR-0010: refresh opaco con rotación, cookie `httpOnly`, access token de 15 minutos y revocación diferida. Falta implementar `security_db` y los endpoints.
- **Contraseñas:** resuelto en ADR-0011: Argon2id, mínimo de 12 caracteres y bloqueo de contraseñas comunes. Falta agregar la dependencia y el validador.
- **Comunicación interna:** falta confirmar si `order-service` llama a `catalog-service` por red interna directa o a través del gateway. La arquitectura sugiere red interna directa, sin exponer el servicio.
- **Auditoría e idempotencia:** falta definir retención, limpieza y responsables.
- **Entornos:** Docker y `.env.example` ya existen; falta CI.
- **Código:** el esqueleto fue autorizado; cada etapa de negocio requiere autorización explícita.

## 8. Próximos pasos

1. Escribir `docs/api/security.openapi.yaml` con registro, login, refresh, logout, perfil y cambio de contraseña.
2. Agregar `security_db` a Docker Compose y crear las migraciones de `users` y `sessions`.
3. Implementar los endpoints de autenticación y el validador de contraseñas.
4. Endurecer el gateway: `typ`, CSRF, cookies, `WWW-Authenticate`, redacción de logs y rotación JWKS.
5. Agregar pruebas E2E y CI antes de la demo.
6. Cerrar ADR-0004 y ADR-0005 para catálogo y pedidos.

## 9. Registro de decisiones

| Fecha | Decisión | Estado |
|---|---|---|
| 2026-11-10 | Usar Prisma con `@prisma/adapter-pg` y `pg` | Confirmado |
| 2026-11-10 | Organizar el backend con npm workspaces | Confirmado |
| 2026-11-10 | Instalar base TypeScript, Vitest, Zod, `jose` y Prisma | Hecho |
| 2026-11-10 | Usar Fastify 5 con plugins por servicio | Confirmado e instalado |
| 2026-11-10 | ADR-0008: ESM, project references y paquete `@perfumespayday/shared` | Aceptado |
| 2026-11-10 | Esqueleto del backend con `/health`, Docker y pruebas | Hecho |
| 2026-11-14 | ADR-0003: JWKS principal y PEM como respaldo | Aceptado |
| 2026-11-14 | ADR-0006: errores, paginación e idempotencia | Aceptado |
| 2026-11-14 | ADR-0009: sesiones, refresh opaco y cookies | Aceptado |
| 2026-11-14 | ADR-0010: access token de 15 minutos sin denylist en beta | Aceptado |
| 2026-11-14 | ADR-0011: Argon2id y política de contraseñas | Aceptado |
| 2026-11-14 | Contrato `security.openapi.yaml` y `security_db` | Pendiente |
