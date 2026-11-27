# ADR-0001 — Microservicios con gateway único

| Campo | Valor |
|---|---|
| Estado | Aceptado |
| Fecha | 2026-11-10 |
| Decisores | Equipo |
| Relacionados | README raíz §5, [`architecture.md`](../architecture.md), diagramas 01 y 02 |

## Contexto

El proyecto es un simulador académico de tienda de perfumes con una beta de 3 semanas y 4 personas. La arquitectura de microservicios es un requisito académico. El sistema debe separar autenticación, catálogo y pedidos, y dejar una puerta de entrada única para la web y la futura app móvil.

## Decisión

Se adopta una arquitectura de microservicios con cuatro contenedores desplegables:

- **Gateway** público, escrito en Node.js + Fastify.
- **security-service** interno, escrito en Python + FastAPI.
- **catalog-service** interno, escrito en Node.js + Fastify.
- **order-service** interno, escrito en Node.js + Fastify.

Cada servicio tiene su propia base de datos PostgreSQL: `security_db`, `catalog_db` y `orders_db`. No hay tablas ni joins compartidos. Solo el gateway se expone a internet.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas | Veredicto |
|---|---|---|---|
| Monolito modular | Menos despliegues y menor complejidad operativa | Incumple el requisito académico de microservicios | Rechazado |
| Dos servicios (API + seguridad) | Menos piezas que mantener | No separa catálogo de pedidos ni demuestra límites de dominio | Rechazado |
| Microservicios con gateway | Cumple el requisito, separa responsabilidades y permite escalar por servicio | Más configuración, red y despliegues | **Aceptado** |
| Serverless | Menos infraestructura | Fuera del stack acordado y difícil de demostrar en 3 semanas | Rechazado |

## Consecuencias

- Cada servicio se despliega y configura por separado.
- El gateway se convierte en un punto único de fallo; debe tener healthcheck y manejo de errores.
- La comunicación interna y la propiedad de datos deben documentarse (ver [ADR-0005](0005-comunicacion-interna.md) y [ADR-0004](0004-propiedad-datos.md)).
- El equipo asume más complejidad operativa, pero obtiene límites claros y cumplimiento académico.
- Docker y Docker Compose son obligatorios para reproducir el entorno.

## Pendientes

- Definir la comunicación interna entre servicios.
- Definir el despliegue y los healthchecks.
- Confirmar la entrega de la clave pública JWT.

## Referencias

- [README raíz §5](../../README.md)
- [`architecture.md`](../architecture.md)
- [`diagrams/01-contexto-sistema.svg`](../diagrams/01-contexto-sistema.svg)
- [`diagrams/02-arquitectura-contenedores.svg`](../diagrams/02-arquitectura-contenedores.svg)
