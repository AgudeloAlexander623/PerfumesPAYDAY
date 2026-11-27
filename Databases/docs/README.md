# Databases

## Tecnologías

- PostgreSQL
- Prisma 7 (decidido; cierre pendiente en [ADR-0004](../../docs/adr/0004-propiedad-datos.md))

## Acceso propuesto desde n8n

- **Estado:** propuesto, sin conexiones ni credenciales creadas (2026-11-26 UTC).
- n8n **no** accede directamente a `security_db`, `catalog_db` ni `orders_db`: si necesita datos, los solicita a los servicios mediante interfaces documentadas.
- Las automatizaciones se limitan a tareas en segundo plano y datos derivados. Las escrituras operativas siguen siendo propiedad exclusiva de cada servicio.
- Decisión: [ADR-0012](../../docs/adr/0012-n8n-fuera-ruta-critica.md). Detalle: [integraciones](../../docs/integrations/README.md).
