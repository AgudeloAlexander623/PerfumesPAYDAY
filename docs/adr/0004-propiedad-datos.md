# ADR-0004 — Propiedad de datos y contrato backend–BD

| Campo | Valor |
|---|---|
| Estado | Propuesto / bloqueante |
| Fecha | 2026-11-10 |
| Decisores | Equipo, responsable de base de datos |
| Relacionados | [`architecture.md`](../architecture.md) §4, CU-07 a CU-25, [`Backend/docs/PLAN.md`](../../Backend/docs/PLAN.md) §7 |

## Contexto

La base de datos es responsabilidad de otra persona del equipo. El backend necesita leer y escribir en `catalog_db` y `orders_db`, pero **no debe diseñar los esquemas por su cuenta**. Hoy el backend tiene instalados `prisma`, `@prisma/client`, `@prisma/adapter-pg` y `pg`, pero no existe un `schema.prisma` ni un contrato de acceso a datos.

Esta decisión bloquea:

- El diseño de catálogo y pedidos.
- Los contratos OpenAPI de `catalog` y `orders`.
- El documento `data-contracts.md`.
- La utilidad real de las dependencias de Prisma y `pg`.

## Decisión

**Pendiente de aprobación.** Se proponen cuatro opciones; la elección debe acordarse con el responsable de la base de datos.

### Opción A — Esquema propiedad de la BD, cliente Prisma consumido por el backend

La persona de BD diseña y mantiene el esquema y las migraciones. El backend solo consume el cliente Prisma generado.

| Ventajas | Desventajas |
|---|---|
| Respeta la propiedad de la BD | El backend depende de la generación del cliente |
| Tipado fuerte y migraciones controladas | Requiere coordinar versiones del esquema |
| Aprovecha Prisma ya instalado | Puede haber fricción si la BD cambia sin avisar |

### Opción B — El backend define el `schema.prisma`

El backend diseña las tablas y migraciones.

| Ventajas | Desventajas |
|---|---|
| Control total del modelo desde el código | **Viola la propiedad de la BD acordada** |
| Menos coordinación | Duplica responsabilidades y genera conflictos |

**Veredicto:** rechazada mientras la BD sea de otra persona.

### Opción C — Contrato SQL y capa de repositorios con `pg`

La persona de BD define tablas, vistas y funciones; el backend usa `pg` con consultas parametrizadas y una capa de repositorios.

| Ventajas | Desventajas |
|---|---|
| Contrato explícito y estable | Más código manual y menos tipado automático |
| La BD conserva el control del esquema | Hay que mantener tipos y mapeos a mano |
| `pg` ya está instalado | Las migraciones siguen siendo de la BD |

### Opción D — La BD expone una API de datos

La persona de BD publica endpoints y el backend consume esa API.

| Ventajas | Desventajas |
|---|---|
| Desacopla por completo | Agrega un servicio y latencia innecesarios para la beta |
| La BD controla todo el acceso | Excede el alcance de 3 semanas |

**Veredicto:** rechazada para la beta.

## Recomendación

- **Opción A** si se conserva Prisma y la persona de BD acepta mantener el esquema y generar el cliente.
- **Opción C** si la persona de BD prefiere SQL explícito o no quiere depender de Prisma.
- En ambos casos, el backend **no** crea tablas ni migraciones por su cuenta.
- Si no se elige A, se deben evaluar y probablemente retirar `prisma`, `@prisma/client` y `@prisma/adapter-pg`.

## Consecuencias

- `data-contracts.md` debe describir entidades, dueño, operaciones permitidas, claves, índices y reglas de integridad.
- Los contratos OpenAPI de catálogo y pedidos se escriben después de esta decisión.
- Las pruebas de integración necesitan una base de datos o un repositorio mockeado.
- Los snapshots de pedidos y la auditoría siguen siendo responsabilidad del backend, aunque las tablas las cree la BD.
- La decisión afecta el `package.json` del backend y el orden de programación.

## Pendientes

- Reunión con el responsable de la base de datos.
- Elegir A o C.
- Definir el mecanismo de migraciones y versionado.
- Definir credenciales por servicio.
- Confirmar si se conservan las dependencias de Prisma.

## Referencias

- [`architecture.md`](../architecture.md) §4
- [`Backend/docs/PLAN.md`](../../Backend/docs/PLAN.md) §5, §7 y §9
- [`Backend/docs/README.md`](../../Backend/docs/README.md) §5
- [CU-17 — Checkout simulado](../use-cases/cu-17-checkout-simulado.md)
