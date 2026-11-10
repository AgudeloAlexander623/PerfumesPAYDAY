# ADR-0008 — Estrategia de módulos TypeScript

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-10 |
| Decisores | Equipo de backend |
| Relacionados | [`Backend/tsconfig.base.json`](../../Backend/tsconfig.base.json), [`Backend/tsconfig.json`](../../Backend/tsconfig.json), [`Backend/packages/shared`](../../Backend/packages/shared), `Backend/services/*/tsconfig.json` |

> Esta versión acepta la propuesta del mismo día y sustituye el borrador. No cambia el alcance: solo fija la opción elegida y cómo se implementó.

## Contexto

`Backend/tsconfig.base.json` usa `"module": "NodeNext"` y `"verbatimModuleSyntax": true`. Los `package.json` de `gateway`, `catalog` y `orders` no declaraban `"type": "module"`, así que TypeScript trataba los archivos `.ts` como CommonJS y rechazaba `import`/`export` de ESM:

```text
TS1295: ECMAScript imports and exports cannot be written in a CommonJS file
under 'verbatimModuleSyntax'. Adjust the 'type' field in the nearest
'package.json' to make this file an ECMAScript module...

TS1287: A top-level 'export' modifier cannot be used on value declarations
in a CommonJS module when 'verbatimModuleSyntax' is enabled.
```

Sin resolver esto no se podía compilar ni arrancar ningún servicio. Además, los tres servicios necesitaban la misma configuración, el mismo formato de errores, el mismo `/health` y el mismo ciclo de vida; repetir esa lógica en cada uno habría creado código redundante.

## Decisión

**Opción A: ESM nativo en todo el workspace.**

- Declarar `"type": "module"` en la raíz del workspace y en cada paquete (`gateway`, `catalog`, `orders`, `shared`).
- Mantener `NodeNext` + `verbatimModuleSyntax` en `tsconfig.base.json`.
- Escribir los imports relativos con extensión `.js` (`import { envSchema } from './config/env.js'`).
- Compilar con `tsc -b` y **project references**: un `tsconfig.json` solución en `Backend/` y uno por paquete.
- Usar `tsx` para desarrollo y `tsc` para producción.
- Concentrar lo transversal en el paquete privado `@perfumespayday/shared`: configuración de entorno, envelope de errores, `/health`, `requestId`, Helmet y ciclo de vida.
- Ejecutar las pruebas con Vitest y un alias que resuelve `@perfumespayday/shared` a su código fuente, sin exigir compilación previa.

Cada servicio queda reducido a su configuración y su punto de entrada:

```text
services/gateway/
├── src/config/env.ts   # Esquema de entorno con su puerto por defecto
├── src/server.ts       # startService({ name, envSchema })
└── tsconfig.json       # Extiende la base y referencia a shared
```

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| **A. ESM nativo** (`type: module`) | Coherente con Node.js 22 y Fastify 5; verificación estricta de imports; estándar moderno | Los imports relativos necesitan `.js`; exige disciplina | **Aceptado** |
| B. Quitar `verbatimModuleSyntax` o usar CommonJS | No exige extensiones `.js`; menos cambios | Pierde verificación estricta; se aleja del estándar | Rechazado |
| C. Archivos `.mts`/`.cts` | Control por archivo | Complejidad innecesaria para tres servicios | Rechazado |

## Consecuencias

- Los imports relativos se escriben con `.js`, también en TypeScript.
- `tsc -b` construye `shared` antes que los servicios; el orden lo resuelven las referencias, no los scripts.
- `npm run dev:*` compila `shared` una vez mediante `predev`; después `tsx` vigila solo el servicio.
- Los tests no dependen del build porque Vitest resuelve `@perfumespayday/shared` al fuente.
- Cualquier paquete nuevo del workspace debe declarar `"type": "module"`.
- El paquete compartido es una dependencia de compilación, no un servicio en ejecución: cada imagen contiene su propia copia compilada.
- VSCode debe usar la versión de TypeScript del workspace para no mezclar configuraciones.

## Verificación

| Comprobación | Resultado |
|---|---|
| `npm run build` | Compila `shared`, `gateway`, `catalog` y `orders` sin errores |
| `npm test` | 7 pruebas en verde (salud, errores y `requestId`) |
| `node services/catalog/dist/server.js` + `GET /health` | `200` con `{"status":"ok","service":"catalog"}` |
| `docker compose build catalog` + contenedor | Imagen construida y `/health` responde `200` |
| Cierre ordenado | `SIGTERM` registra el cierre y termina el proceso |

## Pendientes

- Documentar los comandos en `docs/getting-started.md` cuando se redacte.
- Replicar la convención de ESM en cualquier paquete Node.js que se agregue al workspace.

## Referencias

- [`Backend/tsconfig.base.json`](../../Backend/tsconfig.base.json)
- [`Backend/tsconfig.json`](../../Backend/tsconfig.json)
- [`Backend/packages/shared`](../../Backend/packages/shared)
- [`Backend/docs/ROADMAP.md`](../../Backend/docs/ROADMAP.md)
- [`ADR-0002`](0002-fastify-workspaces.md)
