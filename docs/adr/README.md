# Registro de decisiones de arquitectura (ADR)

Un **ADR** (*Architecture Decision Record*) documenta una decisión importante, su contexto, las alternativas consideradas y sus consecuencias. Sirve para que el equipo sepa **por qué** el sistema es como es y para no repetir discusiones ya cerradas.

> **Regla:** una decisión aceptada no se edita. Si cambia, se crea un ADR nuevo que reemplaza al anterior y se actualiza el estado del anterior.

---

## 1. Estados

| Estado | Significado |
|---|---|
| **Propuesto** | La decisión está redactada, pero el equipo aún no la aprueba. |
| **Aceptado** | La decisión está aprobada y se aplica. |
| **Rechazado** | La opción se evaluó y se descartó. |
| **Reemplazado** | Un ADR posterior la sustituye; se indica cuál. |
| **Bloqueado** | No se puede aprobar hasta resolver una dependencia externa. |

---

## 2. Convenciones

- Archivo: `NNNN-titulo-corto.md`, con número secuencial de cuatro dígitos.
- Título en español y kebab-case.
- Un ADR por decisión; no mezclar temas independientes.
- Fecha en formato ISO 8601 (UTC).
- Los ADR se guardan en `docs/adr/`.
- Los ADR aceptados se enlazan desde [`architecture.md`](../architecture.md) y [`security.md`](../security.md) cuando aplique.
- Las decisiones de API se reflejan en [`api/`](../api/README.md).

---

## 3. Plantilla

```markdown
# ADR-NNNN — Título

| Campo | Valor |
|---|---|
| Estado | Propuesto / Aceptado / Rechazado / Reemplazado |
| Fecha | YYYY-MM-DD |
| Decisores | Equipo |
| Relacionados | ADR-XXXX, CU-XX, documento |

## Contexto

¿Qué problema hay que resolver? ¿Qué restricciones existen?

## Decisión

¿Qué se decide? En los ADR propuestos, indicar que está pendiente de aprobación.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|

## Consecuencias

¿Qué implica la decisión? ¿Qué cambia en el código, la operación o la documentación?

## Pendientes

¿Qué falta para aprobar o implementar la decisión?

## Referencias

Enlaces a documentos, casos de uso o diagramas.
```

---

## 4. Índice

| ADR | Título | Estado | Fecha |
|---|---|---|---|
| [ADR-0001](0001-microservicios-gateway.md) | Microservicios con gateway único | Aceptado | 2026-11-10 |
| [ADR-0002](0002-fastify-workspaces.md) | Fastify 5 y npm workspaces | Aceptado | 2026-11-10 |
| [ADR-0003](0003-jwt-rs256.md) | Entrega de la clave pública JWT | Propuesto | 2026-11-10 |
| [ADR-0004](0004-propiedad-datos.md) | Propiedad de datos y contrato backend–BD | Propuesto / bloqueante | 2026-11-10 |
| [ADR-0005](0005-comunicacion-interna.md) | Comunicación interna `orders` → `catalog` | Propuesto | 2026-11-10 |
| [ADR-0006](0006-errores-paginacion-idempotencia.md) | Errores, paginación e idempotencia | Propuesto | 2026-11-10 |
| [ADR-0007](0007-carrito-hibrido.md) | Carrito híbrido | Aceptado | 2026-11-10 |
| [ADR-0008](0008-modulos-typescript.md) | Estrategia de módulos TypeScript | Aceptado | 2026-11-10 |

---

## 5. Decisiones que bloquean la programación

| ADR | Qué bloquea |
|---|---|
| ADR-0004 | Catálogo, pedidos, dependencias de Prisma y `data-contracts.md`. |
| ADR-0003 | Autenticación real, gateway y despliegue. |
| ADR-0006 | Contratos OpenAPI, manejo de errores y checkout idempotente. |
| ADR-0005 | Llamadas internas de `orders` a `catalog`. |

---

**Última actualización:** 2026-11-10
