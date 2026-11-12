# Documentación del proyecto

Punto de entrada a la documentación global de **PerfumesPAYDAY**. El [README raíz](../README.md) explica el producto, el equipo, la estructura y el alcance; este índice organiza los documentos que desarrollan esos temas.

> **Estado del proyecto:** el backend ya tiene su esqueleto técnico (servicios que compilan, arrancan y responden `/health`). No hay endpoints de negocio, base de datos creada ni contratos implementados. La documentación sigue siendo la fuente de verdad para el resto del desarrollo.

---

## 1. Mapa de documentos

| Documento | Qué responde | Estado | Última actualización |
|---|---|---|---|
| [`../README.md`](../README.md) | Qué es el proyecto, equipo, estructura, stack, flujos, reglas y cronograma | Redactado | 2026-11-10 |
| [`architecture.md`](architecture.md) | Cómo se compone el sistema, qué posee cada servicio y cómo se comunica | Redactado | 2026-11-10 |
| [`security.md`](security.md) | Qué amenazas existen, qué controles se aplican y cómo se prueba la seguridad | Redactado | 2026-11-10 |
| [`beta-criteria.md`](beta-criteria.md) | Cómo se demuestra que la beta está lista | Redactado | 2026-11-11 |
| [`scrum/scrum.md`](scrum/scrum.md) | Sprints, tablero, ceremonias, DoR/DoD y métricas | Redactado | 2026-11-11 |
| [`scrum/technical-stories.md`](scrum/technical-stories.md) | Historias técnicas (habilitadoras) que sostienen las funcionales | Redactado | 2026-11-11 |
| `getting-started.md` | Cómo instalar, ejecutar y probar el proyecto en local | Pendiente | — |
| `testing.md` | Estrategia, herramientas y cobertura de pruebas | Pendiente | — |
| `deployment.md` | Docker, entornos, CI/CD, secretos y despliegue | Pendiente | — |
| `data-contracts.md` | Acuerdo de integración entre el backend y la base de datos | Pendiente | — |
| [`use-cases/`](use-cases/README.md) | Qué debe hacer el sistema: 25 casos de uso y sus prioridades | Redactado | 2026-11-10 |
| [`user-stories/`](user-stories/user-stories.md) | Historias de usuario derivadas de los casos de uso, para el backlog | Redactado | 2026-11-11 |
| [`diagrams/`](diagrams/README.md) | Diagramas de contexto, contenedores y flujos | Redactado | 2026-11-10 |
| [`adr/`](adr/README.md) | Decisiones de arquitectura y su justificación | En progreso | 2026-11-10 |
| [`api/`](api/README.md) | Convenciones y contratos OpenAPI por servicio | En progreso | 2026-11-10 |

### Estados usados

| Estado | Significado |
|---|---|
| **Redactado** | El documento existe y cubre el alcance previsto; puede requerir revisión. |
| **En progreso** | Existe una parte, pero faltan secciones o contratos. |
| **Pendiente** | El documento está acordado en el índice, pero aún no se ha escrito. |
| **Bloqueado** | No se puede completar hasta que se apruebe una decisión (ver ADR). |

---

## 2. Cómo leer la documentación

### Si eres nuevo en el proyecto

1. [README raíz](../README.md): visión, alcance y estructura.
2. Este índice.
3. [`architecture.md`](architecture.md): cómo encajan las piezas.
4. [`use-cases/README.md`](use-cases/README.md): qué debe hacer el sistema.
5. [`diagrams/README.md`](diagrams/README.md): versión visual de los flujos.

### Si vas a programar el backend

1. [`architecture.md`](architecture.md): límites y propiedad de datos.
2. [`adr/README.md`](adr/README.md): decisiones tomadas y pendientes.
3. [`api/README.md`](api/README.md): convenciones y contratos.
4. [`security.md`](security.md): controles obligatorios.
5. [`use-cases/`](use-cases/README.md): comportamiento esperado y criterios de aceptación.

### Si vas a programar el frontend

1. [`use-cases/`](use-cases/README.md): pantallas, flujos y validaciones.
2. [`api/README.md`](api/README.md): rutas, errores, paginación e idempotencia.
3. [`security.md`](security.md): manejo de sesión, tokens y datos personales.
4. [`diagrams/`](diagrams/README.md): flujos de autenticación, carrito y checkout.

### Si trabajas seguridad o base de datos

1. [`security.md`](security.md): amenazas, controles y pruebas.
2. [`architecture.md`](architecture.md): propiedad de datos y comunicación.
3. [`adr/`](adr/README.md): decisiones de autenticación y contrato de datos.
4. `data-contracts.md`: acuerdo backend–BD (pendiente).

### Si vas a evaluar o demostrar la beta

1. [`beta-criteria.md`](beta-criteria.md): criterios verificables y evidencia.
2. [`use-cases/`](use-cases/README.md): comportamiento esperado.
3. [`diagrams/`](diagrams/README.md): recorrido visual.
4. [`scrum/scrum.md`](scrum/scrum.md): plan de sprints y estado del tablero.

---

## 3. Convenciones de documentación

- La documentación se escribe en **español**; los identificadores técnicos, rutas, campos JSON y nombres de archivos de código quedan en **inglés**.
- Los archivos usan **kebab-case**: `beta-criteria.md`, `cu-17-checkout-simulado.md`.
- Las fechas usan **ISO 8601** y zona horaria **UTC**.
- Los identificadores son **UUID**; la moneda es **COP**.
- Cada documento declara su propósito y su alcance al inicio.
- Los enlaces son **relativos** y deben apuntar a archivos existentes.
- No se duplica contenido: si un tema pertenece a otro documento, se enlaza.
- Los estados se actualizan cuando cambia el documento, no solo cuando cambia el código.
- Los cambios de comportamiento actualizan el caso de uso y el contrato OpenAPI en el mismo pull request.
- Las decisiones importantes se registran como **ADR**; no se editan ADR aceptados, se crea uno nuevo que los reemplace.

---

## 4. Fuentes de verdad

| Tema | Fuente de verdad |
|---|---|
| Comportamiento funcional | [`use-cases/`](use-cases/README.md) |
| Historias de usuario (backlog) | [`user-stories/`](user-stories/user-stories.md) |
| Historias técnicas (habilitadoras) | [`scrum/technical-stories.md`](scrum/technical-stories.md) |
| Estructura y comunicación | [`architecture.md`](architecture.md) |
| Decisiones de arquitectura | [`adr/`](adr/README.md) |
| Contratos de API | [`api/`](api/README.md) |
| Controles de seguridad | [`security.md`](security.md) |
| Criterios de aceptación de la beta | [`beta-criteria.md`](beta-criteria.md) |
| Planificación y sprints | [`scrum/scrum.md`](scrum/scrum.md) |
| Stack y alcance general | [README raíz](../README.md) |

---

## 5. Decisiones abiertas

Estas decisiones están documentadas como propuestas y bloquean total o parcialmente otros documentos:

| ADR | Decisión | Impacto |
|---|---|---|
| [ADR-0003](adr/0003-jwt-rs256.md) | Cómo entregar la clave pública JWT a gateway y servicios | Autenticación, despliegue y `security.md` |
| [ADR-0004](adr/0004-propiedad-datos.md) | Contrato backend–base de datos y uso de Prisma | `data-contracts.md`, catálogo, pedidos y dependencias |
| [ADR-0005](adr/0005-comunicacion-interna.md) | Cómo se comunican `orders` y `catalog` | Arquitectura y contratos internos |
| [ADR-0006](adr/0006-errores-paginacion-idempotencia.md) | Formato de errores, paginación e idempotencia | Todos los contratos OpenAPI |

---

## 6. Documentos pendientes y prioridad

### Prioridad alta

- `data-contracts.md`: acuerdo con la persona responsable de la base de datos.
- Enlace y README del tablero de GitHub Projects.

### Prioridad media

- `getting-started.md`: instalación, comandos, puertos y variables de entorno.
- `testing.md`: estrategia de pruebas y gates de CI.
- `deployment.md`: Docker, entornos y despliegue.

### Prioridad baja

- `CONTRIBUTING.md`, plantillas de pull request e issues, guion de demo independiente y glosario extraído del README.

---

## 7. Mantenimiento

- Cada cambio de comportamiento actualiza el caso de uso correspondiente.
- Cada cambio de API actualiza primero el contrato OpenAPI.
- Cada decisión nueva se registra como ADR antes de implementarse.
- Cada sprint actualiza `scrum.md` y los criterios de beta.
- La documentación se revisa en el mismo pull request que el cambio.

---

**Última actualización:** 2026-11-11
**Responsable:** equipo PerfumesPAYDAY
