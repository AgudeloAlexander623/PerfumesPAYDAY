# ADR-0008 — Estrategia de módulos TypeScript

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-10 |
| Decisores | Equipo de backend |
| Relacionados | [`Backend/tsconfig.base.json`](../../Backend/tsconfig.base.json), `Backend/services/*/package.json` |

## Contexto

`Backend/tsconfig.base.json` usa `"module": "NodeNext"` y `"verbatimModuleSyntax": true`. Los `package.json` de `gateway`, `catalog` y `orders` no declaran `"type": "module"`. Como consecuencia, TypeScript trata los archivos `.ts` como CommonJS y rechaza los `import`/`export` de ESM con errores:

```text
TS1295: ECMAScript imports and exports cannot be written in a CommonJS file
under 'verbatimModuleSyntax'. Adjust the 'type' field in the nearest
'package.json' to make this file an ECMAScript module...

TS1287: A top-level 'export' modifier cannot be used on value declarations
in a CommonJS module when 'verbatimModuleSyntax' is enabled.
```

El problema apareció al abrir un archivo `.ts` de ejemplo en VSCode. No hay código de aplicación todavía, pero la configuración debe resolverse antes de escribir el esqueleto de los servicios.

## Decisión propuesta

**Opción A — declarar `"type": "module"` en cada servicio.**

Agregar `"type": "module"` al `package.json` de `gateway`, `catalog` y `orders`, y mantener `NodeNext` + `verbatimModuleSyntax`.

| Ventajas | Desventajas |
|---|---|
| Coherente con Node.js 22 y Fastify 5 | Las importaciones relativas necesitan extensión `.js` en el código TypeScript |
| Mantiene la verificación estricta de imports | Requiere disciplina en todos los archivos |
| Alinea el backend con el ecosistema ESM | Puede complicar algunas herramientas si no soportan ESM |

**Opción B — quitar `verbatimModuleSyntax` o cambiar a CommonJS.**

Mantener `module: NodeNext` sin `verbatimModuleSyntax`, o cambiar a `module: CommonJS`.

| Ventajas | Desventajas |
|---|---|
| No exige extensiones `.js` en imports relativos | Se pierde la verificación estricta de imports |
| Menos cambios en el código | Se aleja del estándar ESM de Node.js moderno |
| Funciona con herramientas antiguas | Puede generar deuda técnica |

**Opción C — archivos `.mts`/`.cts`.**

Usar extensiones explícitas por archivo.

| Ventajas | Desventajas |
|---|---|
| Control total por archivo | Innecesariamente complejo para tres servicios |

## Recomendación

**Opción A.** Es la más coherente con Node.js 22, Fastify 5 y el `tsconfig.base.json` actual. Si el equipo prefiere evitar las extensiones `.js`, la Opción B es válida, pero debe aplicarse de forma uniforme y documentarse.

## Consecuencias

- Si se elige A, los imports relativos se escriben con `.js` (por ejemplo, `import { env } from './config/env.js'`).
- `tsx` se usa para desarrollo y `tsc` para compilar.
- Los tests de Vitest deben configurarse para ESM.
- La decisión aplica a los tres servicios, no solo al gateway.
- Hay que agregar un `tsconfig.json` por servicio que extienda `tsconfig.base.json`.

## Pendientes

- Aprobar A o B.
- Agregar `"type": "module"` o ajustar `tsconfig.base.json`.
- Crear el `tsconfig.json` de cada servicio.
- Verificar que VSCode use la misma configuración que el compilador del workspace.
- Documentar la convención de imports en `getting-started.md`.

## Referencias

- [`Backend/tsconfig.base.json`](../../Backend/tsconfig.base.json)
- [`Backend/package.json`](../../Backend/package.json)
- [`Backend/services/gateway/package.json`](../../Backend/services/gateway/package.json)
- [`Backend/docs/PLAN.md`](../../Backend/docs/PLAN.md) §7
