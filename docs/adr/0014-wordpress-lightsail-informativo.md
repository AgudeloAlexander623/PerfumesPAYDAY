# ADR-0014 — WordPress en Lightsail solo como canal informativo

| Campo | Valor |
|---|---|
| Estado | Propuesto |
| Fecha | 2026-11-26 |
| Decisores | Equipo (pendiente de aprobación) |
| Relacionados | [Integraciones](../integrations/README.md), [Seguridad](../security.md), [ADR-0001](0001-microservicios-gateway.md) |

## Contexto

El equipo propone usar AWS Lightsail con WordPress. WordPress es un CMS orientado a contenido, no a ejecutar la API de una tienda con microservicios. Integrarlo en el flujo de la aplicación duplicaría despliegues y ampliaría la superficie de ataque.

## Decisión

Usar Lightsail con WordPress **únicamente** como sitio informativo, blog y material de demostración. No alojará gateway, microservicios, PostgreSQL, credenciales ni secretos. El repositorio sigue siendo la fuente de verdad de la documentación. Toda creación de instancia requiere HTTPS, actualizaciones, copias de seguridad, acceso restringido y revisión de seguridad previa.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| WordPress como frontend de la tienda | Familiar para el equipo | Mezcla roles, duplica lógica y expone CMS | Rechazada |
| WordPress solo como blog | Contenido separado de la API | Requiere mantenimiento propio | **Seleccionada** |
| No publicar sitio informativo | Menos superficie | Menos material para la demo | Rechazada |

## Consecuencias

- La API y la web siguen desplegándose por su propia vía; nada depende del CMS.
- El sitio queda fuera de los criterios de beta y no consulta bases de datos del proyecto.
- Debe documentarse como activo externo si llega a crearse.

## Pendientes

- Aprobación del ADR y definición de responsable del sitio.
- Revisión de plugins, actualizaciones, copias y control de acceso.
- Confirmar que no se publican secretos ni enlaces internos.

## Referencias

- [Integraciones y operación](../integrations/README.md)
- [Arquitectura del sistema](../architecture.md)
- [Seguridad del sistema](../security.md)
