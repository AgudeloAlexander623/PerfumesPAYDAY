# Integraciones y operación (propuesto)

> **Estado:** propuesto. Ninguna de estas integraciones está implementada, configurada ni autorizada para la beta. Esta página solo registra alcance, límites y decisiones pendientes.
> **Fecha:** 2026-11-26 (UTC)

---

## 1. Propósito

Dejar por escrito qué se espera de **n8n**, el monitoreo **SRE**, **AWS Lightsail con WordPress** y **Vercel**, antes de tocar código, contratos o infraestructura. No reemplaza los [casos de uso](../use-cases/README.md), los [contratos de API](../api/README.md) ni los [ADR aceptados](../adr/README.md).

## 2. Principios

- **Fuera de la ruta crítica:** login, carrito, checkout y búsqueda siguen respondiendo en los servicios.
- **Un ADR por decisión:** ninguna integración se implementa sin ADR aceptado y autorización explícita.
- **La beta no depende de ellas:** se registran como trabajo futuro, no como criterios `Must`.
- **Un responsable por integración:** secretos fuera del repositorio y telemetría sin datos personales.

## 3. Mapa de integraciones

| Tema | Para qué sirve | Decisión | Estado |
|---|---|---|---|
| n8n | Automatizaciones en segundo plano: *seeds*, mantenimiento de tags/sinónimos, agregación de auditoría, avisos y reportes | [ADR-0012](../adr/0012-n8n-fuera-ruta-critica.md) | Propuesto |
| SRE | Métricas, logs con `requestId`, alertas y objetivos de nivel de servicio | [ADR-0013](../adr/0013-monitoreo-sre.md) | Propuesto |
| AWS Lightsail + WordPress | Sitio informativo y blog del proyecto; nunca la API ni las bases de datos | [ADR-0014](../adr/0014-wordpress-lightsail-informativo.md) | Propuesto |
| Vercel | Alojamiento del frontend web con HTTPS | [ADR-0015](../adr/0015-frontend-vercel.md) | Propuesto |

## 4. Detalle por integración

### 4.1 n8n

- Ejecuta tareas programadas o disparadas por eventos, siempre sobre datos de apoyo o derivados.
- **No** interviene en `/api/v1/*`, en la validación JWT ni en la búsqueda en tiempo real.
- Si necesita información, la solicita a los servicios mediante interfaces documentadas; **no escribe directamente** en `security_db`, `catalog_db` ni `orders_db`.
- Las consultas por marca y color se resuelven con atributos etiquetados en el catálogo. n8n puede mantener esos atributos en segundo plano, nunca decidir la respuesta de una búsqueda.

### 4.2 SRE

- Objetivo: observabilidad basada en latencia, errores y saturación, con logs JSON y `requestId`, alertas accionables y presupuestos de error.
- Se apoya en los [requisitos no funcionales](../architecture.md#9-requisitos-no-funcionales) y en las reglas de [logs y privacidad](../security.md#11-logs-auditoría-y-privacidad).
- Antes de instrumentar se definen: señales concretas, umbrales, retención, responsable de guardia y qué datos quedan excluidos (tokens, contraseñas, direcciones y cuerpos de petición).

### 4.3 AWS Lightsail + WordPress

- Uso previsto: blog, notas de avance y material de demostración, separado de la API.
- **No** aloja el gateway, los microservicios, PostgreSQL ni secretos. El repositorio sigue siendo la fuente de verdad de la documentación.
- Requisitos previos a cualquier creación: HTTPS, actualizaciones al día, copias de seguridad, acceso restringido y revisión de [seguridad](../security.md).

### 4.4 Vercel

- Uso previsto: despliegue del frontend estático (React + Vite) con URL pública y HTTPS.
- El [gateway](../architecture.md#3-contenedores) continúa siendo el único punto público de la API; CORS queda restringido a los orígenes reales.
- Los secretos nunca se incluyen en el *bundle*; las variables públicas se documentan antes de usarse y los *preview deployments* se revisan como cualquier cambio.

## 5. Relación con la beta

| Elemento | ¿Está en la beta? | Detalle |
|---|---|---|
| n8n, SRE, WordPress, Vercel | No | No aparecen en los 18 casos `Must` ni en los criterios B/S/Q/I de [beta-criteria.md](../beta-criteria.md). |
| Documentación de estas piezas | Sí | Este documento y los ADR 0012 a 0015 quedan registrados como propuestos. |

## 6. Checklist antes de autorizar

- [ ] ADR-0012, ADR-0013, ADR-0014 y ADR-0015 aceptados.
- [ ] Responsable designado para cada integración.
- [ ] Impacto reflejado en `architecture.md`, `security.md` y contratos si aplica.
- [ ] Costes, cuentas y acceso definidos.
- [ ] Revisión de seguridad sin secretos ni exposición interna.
- [ ] Autorización explícita del líder del proyecto.

## 7. Referencias

- [Arquitectura](../architecture.md) · [Seguridad](../security.md) · [Plan del backend](../PLAN.md) · [Roadmap](../ROADMAP.md)
- [Criterios de beta](../beta-criteria.md) · [ADR](../adr/README.md)
- [Frontend](../../Frontend/docs/README.md) · [Backend](../../Backend/docs/README.md) · [Bases de datos](../../Databases/docs/README.md)

## 8. Mantenimiento

Los cambios de estado se registran en el ADR correspondiente; un ADR aceptado no se edita, se reemplaza por uno nuevo. Se mantienen las convenciones de [docs/README.md](../README.md): español, fechas ISO 8601 UTC y enlaces relativos.

---

**Última actualización:** 2026-11-26
**Estado:** propuesto — sin implementación
