# Plan de trabajo (Scrum / Kanban) — PerfumesPAYDAY

> **Estado:** redactado — pendiente de validación con el equipo.
> **Última actualización:** 2026-11-11
> **Fuente de verdad del trabajo:** el **tablero de GitHub Projects**. Este documento define *cómo* se trabaja (ceremonias, DoR, DoD, sprints y métricas).
> **Documentos relacionados:** [`../user-stories/`](../user-stories/user-stories.md) (historias de usuario), [`technical-stories.md`](technical-stories.md) (historias técnicas), [`../beta-criteria.md`](../beta-criteria.md) (criterios de aceptación), [`../../README.md`](../../README.md) (alcance y cronograma).

---

## 1. Propósito

Definir el marco de trabajo del proyecto para que el equipo, el profesor y los asistentes de IA tengan reglas claras: **qué** se construye en cada sprint, **cuándo** una historia está lista para empezar y **cuándo** está terminada. El proyecto dura **3 semanas** con **4 personas** y metodología **Scrum/Kanban** (README, sección 11).

---

## 2. Metodología

Se usa un **Scrum ligero con tablero Kanban**: el trabajo se planifica en sprints de una semana, pero el flujo diario se visualiza y limita en el tablero.

- **3 sprints de 1 semana** alineados con las semanas del cronograma del README.
- **WIP limitado** por columna para no abrir trabajo sin cerrarlo.
- **Sin ceremonias pesadas:** lo mínimo para mantener el ritmo y la visibilidad.

---

## 3. Equipo y roles

| Rol | Responsable | Responsabilidad |
|---|---|---|
| Product Owner | *Por confirmar* | Prioriza el backlog, define criterios de aceptación y acepta el incremento. |
| Líder técnico | *Por confirmar* | Decisiones de arquitectura (ADRs) y revisión técnica. |
| Equipo de desarrollo | *Por confirmar* | Implementa las historias, escribe pruebas y documenta. |
| Scrum Master (rotativo) | El equipo | Facilita ceremonias, quita bloqueos y cuida el tablero. |

> ⚠️ **Riesgo abierto:** 3 de los 4 roles del README figuran como "Pendiente". Deben confirmarse antes del Sprint 1 o el alcance se recorta a solo los Must.

---

## 4. Artefactos

| Artefacto | Dónde vive | Contenido |
|---|---|---|
| Product Backlog | Tablero (GitHub Projects) | 25 historias de usuario (HU-01 a HU-25) + 15 técnicas (HT-01 a HT-15, en [`technical-stories.md`](technical-stories.md)). |
| Sprint Backlog | Vista por sprint del tablero | Historias comprometidas en el sprint. |
| Incremento | Repositorio | Código, pruebas y documentación de lo terminado. |
| Definition of Ready | Sección 5 | Cuándo una historia puede entrar a un sprint. |
| Definition of Done | Sección 6 | Cuándo una historia está terminada. |
| Criterios de beta | [`../beta-criteria.md`](../beta-criteria.md) | Contrato de aceptación final. |

---

## 5. Definition of Ready (DoR)

Una historia puede **entrar a un sprint** solo si cumple **todo** lo siguiente:

- [ ] Tiene objetivo claro y un único resultado esperado.
- [ ] Tiene criterios de aceptación verificables (formato Dado/Cuando/Entonces).
- [ ] Está trazada a un caso de uso (`CU-XX`) y a una épica.
- [ ] Sus dependencias están identificadas y resueltas o planificadas.
- [ ] Tiene prioridad asignada (Must / Should / Could).
- [ ] Está estimada por el equipo.
- [ ] Si toca la API, el **contrato OpenAPI está definido antes** de implementar (regla del proyecto).
- [ ] Si requiere diseño de interfaz, el diseño está disponible.
- [ ] No depende de una pregunta abierta sin resolver que la bloquee.

Si una historia no cumple el DoR, se devuelve al backlog; no se abre trabajo a medias.

---

## 6. Definition of Done (DoD)

Una historia está **terminada** solo si cumple **todo** lo siguiente:

- [ ] Todos sus criterios de aceptación se demuestran.
- [ ] Existe una **prueba automática** cuando el criterio lo permite (obligatoria en seguridad e idempotencia).
- [ ] La autorización se valida **en el servidor**, no solo en la interfaz.
- [ ] La interfaz es usable en celular, tablet y computador, sin desplazamiento horizontal.
- [ ] Hay estados de carga y de error claros; los errores no exponen detalles internos.
- [ ] El *lint* y las pruebas pasan; la **integración continua está en verde**.
- [ ] El código fue revisado y aprobado en un **pull request** por otra persona.
- [ ] La documentación del componente, el caso de uso y el contrato OpenAPI quedan actualizados **en el mismo pull request**.
- [ ] No se subieron secretos, tokens ni archivos `.env` reales.

Una historia sin prueba (cuando aplica) o sin CI verde **no** se marca como terminada.

---

## 7. Ceremonias

| Ceremonia | Cuándo | Duración | Resultado |
|---|---|---|---|
| Sprint Planning | Inicio de cada semana | 45 min | Sprint Backlog comprometido y objetivo del sprint. |
| Daily | Diaria | 15 min | Bloqueos visibles y tablero al día. |
| Refinamiento | A mitad de sprint | 30 min | Historias del siguiente sprint cumplen el DoR. |
| Sprint Review | Fin de semana | 30 min | Incremento demostrado contra los criterios. |
| Retrospectiva | Fin de semana | 20 min | Una mejora concreta para el siguiente sprint. |

> En un proyecto de 3 semanas, cada ceremonia debe ser breve y con resultado concreto. Si no produce un acuerdo o un cambio, se recorta.

---

## 8. Sprints

Los tres sprints coinciden con las semanas del README (sección 14). Las fechas exactas se fijan en la planeación.

### Sprint 1 — Fundaciones y flujo mínimo

- **Objetivo:** tener un flujo mínimo de punta a punta: autenticación, catálogo de lectura y SPA base.
- **Historias:** HU-01, HU-02, HU-03, HU-04, HU-08, HU-10.
- **Técnicas:** HT-01 (docker-compose), HT-05 (despliegue inicial), HT-06 (autorización en servidor), HT-07 (CI), HT-08 (gateway), HT-09 (contratos OpenAPI), HT-10 (Prisma y migraciones), HT-11 (paquete compartido), HT-12 (errores estándar), HT-14 (secretos), HT-15 (arnés de pruebas).
- **Puerta de salida:** un usuario se registra, inicia sesión y ve el catálogo desde la URL desplegada.
- **Riesgo:** la infraestructura y la seguridad deben quedar listas antes que las funcionalidades.

### Sprint 2 — Tienda funcional

- **Objetivo:** completar la compra de punta a punta y la administración básica.
- **Historias:** HU-09, HU-12, HU-13, HU-14, HU-15, HU-16, HU-17, HU-18, HU-19, HU-20, HU-21, HU-22.
- **Técnicas:** HT-02 (seed de productos), HT-13 (logs sin datos sensibles).
- **Puerta de salida:** se simula una compra completa (carrito → direcciones → checkout → historial) y el admin gestiona productos.
- **Riesgo:** es el sprint más cargado (12 historias). Si el equipo es menor a 4 personas, se recortan las Should y se protege el checkout.

### Sprint 3 — Seguridad y cierre

- **Objetivo:** endurecer, probar, documentar y desplegar la versión final.
- **Historias:** HU-05, HU-06, HU-07, HU-11, HU-23, HU-24, HU-25.
- **Técnicas:** HT-03 (rate limit), HT-04 (CORS y cabeceras), HT-05 (despliegue final).
- **Puerta de salida:** los criterios de [`../beta-criteria.md`](../beta-criteria.md) en verde y el guion de demo ensayado.
- **Riesgo:** no se debe dejar la seguridad para el final; HT-03 y HT-04 se preparan durante el Sprint 2.

> Los IDs Should/Could (HU-05, HU-06, HU-11, HU-23, HU-24, HU-25) son los primeros en recortarse si el tiempo aprieta. **Nunca** se recorta seguridad ni checkout.

---

## 9. Tablero de GitHub Projects

El tablero es la **fuente de verdad del trabajo**. Su estructura (para la planeación detallada):

**Columnas (flujo):**

`Backlog → Ready → In Progress → In Review → Done`  (más `Blocked` como etiqueta, no como columna).

**Swimlanes (épicas):** EP-01 Cuentas y sesión · EP-02 Catálogo · EP-03 Carrito · EP-04 Checkout y pedidos · EP-05 Administración.

**Campos por tarjeta:** `ID` (HU-XX/HT-XX), `Prioridad` (Must/Should/Could), `Épica`, `Sprint` (1/2/3), `Estimación`, `Responsable`, `Caso de uso` (enlace a `CU-XX`).

**Etiquetas:** `tipo:hu` / `tipo:ht`, `prioridad:must` / `should` / `could`, `bloqueado`, `seguridad`.

**Vistas sugeridas:** por Sprint, por Épica, por Prioridad, y una vista de bloqueados.

> El README del tablero (documento que describe el tablero dentro del repositorio) se creará en la planeación paso a paso. El tablero ya existe en GitHub; falta enlazarlo y documentarlo.

---

## 10. Métricas

| Métrica | Qué mide | Meta |
|---|---|---|
| Velocidad del sprint | Historias terminadas por semana | Cerrar los 18 Must en 3 sprints |
| Quema de alcance | Must restantes vs. días restantes | Sin desviación al final del Sprint 2 |
| Estado de CI | *Pipeline* verde/rojo | Siempre verde antes del merge |
| Cobertura de pruebas | Criterios con prueba automática | Los de seguridad e idempotencia, al 100 % |
| Riesgos abiertos | Riesgos activos | Cero riesgos altos sin plan al cierre |

---

## 11. Gestión de riesgos

| Riesgo | Prob. | Impacto | Mitigación | Dueño |
|---|---|---|---|---|
| Equipo incompleto (3 roles pendientes) | Alta | Alto | Confirmar roles antes del Sprint 1 o recortar a Must | PO |
| Sprint 2 sobrecargado (12 historias) | Alta | Alto | Recortar Should y proteger checkout | PO / equipo |
| ADRs abiertos bloquean contratos | Alta | Medio | Cerrar ADR-0004, 0003 y 0006 en el Sprint 1 | Líder técnico |
| Sin CI desde el inicio | Media | Medio | Implementar HT-07 en el Sprint 1 | Equipo |
| Scope creep (Should/Could se cuelan) | Media | Medio | Nada Should hasta cerrar los 18 Must | PO |
| Ramas dispersas sin PR | Media | Bajo | Consolidar y cerrar ramas en el Sprint 1 | PO |
| Seguridad al final | Media | Alto | Adelantar HT-03 y HT-04 al Sprint 2 | Equipo |

---

## 12. Herramientas y respaldo

- **GitHub Projects:** fuente de verdad del trabajo (backlog, sprints, estados).
- **Repositorio Git:** código, documentación y contratos.
- **Obsidian (respaldo):** el proyecto es Markdown puro, así que `docs/` se puede abrir como *vault* de Obsidian como **copia de seguridad de lectura** para el PO. **No es fuente de verdad**: los cambios se hacen en el repositorio y, si acaso, se copian al *vault*. Nunca se edita el *vault* como origen.
- **`.github/workflows/`:** integración continua (HT-07).

---

## 13. Reglas de trabajo

Tomadas del README (sección 12):

- **Ramas cortas:** `feat/`, `fix/`, `docs/`, `chore/`.
- **Conventional Commits:** `feat(catalog): agregar filtro por marca`.
- **Pull requests:** toda rama se integra por PR, revisada por otra persona, con CI en verde y documentación actualizada.
- **Idioma:** código y variables en inglés; documentación y comentarios en español.
- **Datos:** fechas en ISO 8601 UTC, IDs en UUID, moneda COP.
- **Seguridad:** no se suben secretos; se versiona solo `.env.example`.

---

**Versión:** 0.1
**Responsable:** Product Owner
