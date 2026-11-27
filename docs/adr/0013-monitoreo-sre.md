# ADR-0013 — Monitoreo SRE de la beta

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-26 |
| Decisores | Equipo (pendiente de aprobación) |
| Relacionados | [Integraciones](../integrations/README.md), [Arquitectura](../architecture.md), [Seguridad](../security.md) |

## Contexto

Los servicios ya propagan `requestId` y los logs se describen como JSON estructurado, pero no hay métricas, alertas ni objetivos de nivel de servicio definidos. El proyecto es una beta académica de tres semanas, sin SLA formal y con restricciones de privacidad.

## Decisión

Adoptar primero las **señales y la metodología**: latencia, errores y saturación por servicio; logs con `requestId`; alertas accionables y un presupuesto de error simple. El producto concreto de observabilidad se elige en un ADR posterior, para no fijar una herramienta sin evaluarla. La telemetría excluye tokens, contraseñas, direcciones y cuerpos de petición.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| Solo logs actuales | Cero coste inicial | No detecta degradación ni saturación | Rechazada |
| Plataforma completa desde el inicio | Todo en un lugar | Coste y tiempo incompatibles con la beta | Rechazada |
| Señales y umbrales primero, herramienta después | Bajo coste, decisiones reversibles | Requiere disciplina documental | **Seleccionada** |

## Consecuencias

- `architecture.md` y `security.md` deberán reflejar métricas, retención y exclusión de datos.
- Cada alerta necesita un responsable y una acción esperada; sin eso no se crea.
- Los criterios de beta no cambian: el monitoreo es trabajo futuro.

## Pendientes

- Aprobación del ADR y elección del responsable de guardia.
- Definir umbrales iniciales, retención y presupuesto de error.
- Evaluar herramientas en un ADR nuevo antes de instalar nada.

## Referencias

- [Integraciones y operación](../integrations/README.md)
- [Requisitos no funcionales](../architecture.md#9-requisitos-no-funcionales)
- [Logs, auditoría y privacidad](../security.md#11-logs-auditoría-y-privacidad)
