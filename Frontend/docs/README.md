# Frontend

## Tecnologías

- Vite
- React
- TypeScript
- Tailwind CSS
- React Router
- TanStack Query
- Zustand

## Despliegue propuesto (Vercel)

- **Estado:** propuesto, sin despliegue ni configuración aplicada (2026-11-26 UTC).
- Vercel alojaría el frontend estático (Vite) con HTTPS; el gateway sigue siendo el único punto público de la API.
- Antes de autorizar: documentar build y variables públicas, revisar CORS y confirmar que no haya secretos en el *bundle* ni en los *preview deployments*.
- Decisión: [ADR-0015](../../docs/adr/0015-frontend-vercel.md). Detalle: [integraciones](../../docs/integrations/README.md).
