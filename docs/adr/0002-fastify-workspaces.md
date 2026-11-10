# ADR-0002 — Fastify 5 y npm workspaces

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-10 |
| Decisores | Equipo |
| Relacionados | [`Backend/docs/PLAN.md`](../../Backend/docs/PLAN.md) §3 y §6, [`Backend/docs/README.md`](../../Backend/docs/README.md) §3 |

## Contexto

El backend necesita un framework HTTP para tres servicios Node.js pequeños, un equipo de 4 personas y una beta de 3 semanas. También necesita compartir herramientas de desarrollo sin duplicar dependencias ni configuración.

## Decisión

- Usar **Fastify 5** como framework HTTP en `gateway`, `catalog-service` y `order-service`.
- Usar **npm workspaces** para organizar los tres servicios dentro de `Backend/`.
- Instalar los plugins de Fastify en cada servicio, no en la raíz, salvo herramientas compartidas.
- Mantener `typescript`, `tsx`, `vitest`, `@vitest/coverage-v8` y `prisma` como herramientas de desarrollo en la raíz del workspace.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| Fastify 5 + workspaces | Ligero, rápido, plugins oficiales, poca estructura impuesta | Menos convenciones; el equipo debe definir la organización | **Aceptado** |
| NestJS | Estructura, inyección de dependencias y convenciones | Más peso y tiempo de aprendizaje para 3 semanas | Rechazado |
| Express | Muy conocido y simple | Menos rendimiento y menos validación/esquemas integrados | Rechazado |
| Un `package.json` por servicio sin workspace | Aislamiento total | Duplica configuración y dependencias | Rechazado |

## Consecuencias

- El workspace puede hoistar dependencias y ocultar una que falte en un servicio; hay que verificar con `npm ls` al agregar paquetes.
- Fastify no impone una estructura de carpetas; la organización se documenta en `architecture.md` y en el README del backend.
- Los plugins del gateway (`cors`, `helmet`, `rate-limit`, `http-proxy`) se instalan solo en el gateway.
- `catalog-service` y `order-service` solo necesitan `fastify` y `helmet` mientras no sean públicos.
- La configuración TypeScript compartida vive en `Backend/tsconfig.base.json`.

## Pendientes

- Confirmar la estrategia de módulos TypeScript ([ADR-0008](0008-modulos-typescript.md)).
- Verificar que cada servicio declare sus dependencias reales y no dependa de las hoisteadas.
- Definir la estructura interna de carpetas de cada servicio.

## Referencias

- [`Backend/docs/PLAN.md`](../../Backend/docs/PLAN.md)
- [`Backend/docs/README.md`](../../Backend/docs/README.md)
- [`Backend/package.json`](../../Backend/package.json)
