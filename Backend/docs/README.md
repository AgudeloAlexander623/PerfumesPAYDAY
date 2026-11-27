# Backend

## Tecnologías

- Node.js
- TypeScript
- Fastify 5 (decidido: [ADR-0002](../../docs/adr/0002-fastify-workspaces.md))
- REST / JSON
- Docker

## Observabilidad propuesta (SRE)

- **Estado:** propuesto, sin instrumentación adicional (2026-11-26 UTC).
- Señales previstas: latencia, errores y saturación por servicio, además de logs JSON con `requestId`.
- La telemetría no debe incluir tokens, contraseñas, direcciones ni cuerpos de petición. La herramienta concreta se elige en un ADR posterior.
- Decisión: [ADR-0013](../../docs/adr/0013-monitoreo-sre.md). Detalle: [integraciones](../../docs/integrations/README.md).
