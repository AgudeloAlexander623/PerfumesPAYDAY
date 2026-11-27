# ADR-0012 — n8n fuera de la ruta crítica

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-26 |
| Decisores | Equipo (pendiente de aprobación) |
| Relacionados | [Integraciones](../integrations/README.md), [ADR-0004](0004-propiedad-datos.md), [CU-08](../use-cases/cu-08-buscar-filtrar-productos.md) |

## Contexto

El equipo quiere facilitar la búsqueda de perfumes por atributos concretos, por ejemplo marca y color. Se evaluó usar n8n para resolver esas consultas. n8n añade una capa externa a la petición del usuario, con latencia y acoplamiento adicionales, mientras el catálogo ya puede ofrecer atributos etiquetados y filtros.

## Decisión

Usar n8n **solo** para automatizaciones en segundo plano: sembrar datos, mantener tags y sinónimos, agregar auditoría, generar avisos y reportes. La búsqueda en tiempo real y cualquier escritura crítica se resuelven dentro de los servicios, sin pasar por n8n. n8n no llama directamente a las bases de datos.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| n8n en la ruta de búsqueda | Flujos visuales rápidos | Latencia, acoplamiento y dependencia externa en cada consulta | Rechazada |
| n8n solo en tareas offline | Automatiza sin afectar al usuario | Requiere definir interfaces y responsables | **Seleccionada** |
| Sin automatización | Menos piezas | Trabajo manual repetitivo y sin trazabilidad | Rechazada |

## Consecuencias

- La búsqueda sigue siendo propiedad de `catalog-service` y usa atributos etiquetados.
- n8n necesita interfaces documentadas y credenciales con mínimo privilegio.
- El riesgo de doble clic, reintentos o precio manipulado no se desplaza a la automatización.

## Pendientes

- Aprobación del ADR y designación de responsable.
- Definir qué tareas se automatizan primero y cómo se supervisan.
- Revisar el impacto en `security.md` antes de cualquier conexión.

## Referencias

- [Integraciones y operación](../integrations/README.md)
- [Casos de uso](../use-cases/README.md)
- [Arquitectura](../architecture.md)
