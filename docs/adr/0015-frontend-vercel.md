# ADR-0015 — Frontend web en Vercel

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-26 |
| Decisores | Equipo (pendiente de aprobación) |
| Relacionados | [Integraciones](../integrations/README.md), [Arquitectura](../architecture.md), [Seguridad](../security.md) |

## Contexto

La beta necesita una URL pública con HTTPS para el frontend. La aplicación web es estática (React + Vite + TypeScript) y consume la API exclusivamente a través del gateway. El equipo evalúa Vercel como proveedor de alojamiento.

## Decisión

Desplegar el frontend en Vercel cuando el equipo lo autorice. El gateway continúa siendo el único punto público de la API. El despliegue debe respetar CORS con orígenes explícitos, secretos fuera del *bundle*, variables documentadas y revisión de los *preview deployments*. Este ADR no cambia contratos OpenAPI ni la lógica de los servicios.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| Vercel para el frontend | HTTPS y despliegue rápido | Dependencia de un proveedor externo | **Seleccionada** |
| Mismo proveedor que la API | Un solo lugar | Mayor configuración y acoplamiento | Rechazada |
| WordPress en Lightsail como web | CMS conocido | Mezcla contenidos con aplicación y añade riesgo | Rechazada |

## Consecuencias

- `Frontend/docs/README.md` y `deployment.md` deberán documentar variables y build cuando se apruebe.
- La revisión de CORS y secretos pasa a ser obligatoria antes de publicar.
- La beta no queda bloqueada: hoy el frontend se ejecuta en local con Vite.

## Pendientes

- Aprobación del ADR y definición de la cuenta y el responsable del despliegue.
- Documentar comandos de build, variables públicas y dominios permitidos.
- Verificar que ningún secreto quede en el cliente.

## Referencias

- [Integraciones y operación](../integrations/README.md)
- [Arquitectura del sistema](../architecture.md)
- [Contratos de API](../api/README.md)
