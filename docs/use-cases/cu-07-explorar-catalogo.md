# CU-07 — Explorar catálogo

| Campo | Valor |
|---|---|
| Módulo | Catálogo |
| Actores | Visitante y Cliente (principal) |
| Prioridad | Must |
| Diagrama | [`04-catalogo`](../diagrams/04-catalogo.svg) |

## Objetivo

Mostrar los perfumes disponibles de forma paginada para que el usuario pueda descubrir productos sin necesidad de iniciar sesión.

## Precondiciones

- Ninguna. El catálogo es público.

## Disparador

El usuario abre la página principal o selecciona **Catálogo**.

## Flujo principal

1. El frontend solicita la primera página de productos al gateway.
2. El gateway enruta la petición a `catalog-service`.
3. `catalog-service` consulta `catalog_db` y trae solo productos activos.
4. Une cada producto con su marca, categoría y presentaciones.
5. Calcula el precio desde la presentación más económica y el stock total.
6. Devuelve la página con productos y datos de paginación.
7. El frontend muestra una cuadrícula con imagen, marca, nombre, precio y disponibilidad.
8. El usuario puede cambiar de página.

## Flujos alternativos

### A1 — No hay productos activos

- **Cuándo ocurre:** el catálogo está vacío o todos los productos están desactivados.
- **Respuesta del sistema:** el frontend muestra un estado vacío con un mensaje claro, sin errores técnicos.

### A2 — Página fuera de rango

- **Cuándo ocurre:** se solicita una página que no existe.
- **Respuesta del sistema:** responde `400` o devuelve la última página disponible; el frontend corrige la navegación.

### A3 — Servicio no disponible

- **Cuándo ocurre:** `catalog-service` o la base de datos no responden.
- **Respuesta del sistema:** responde `503`; el frontend muestra un mensaje de reintento.

## Postcondiciones

- El usuario visualiza los productos activos de la página solicitada.

## Reglas de negocio

- Solo se muestran productos con estado `active`.
- El precio se expresa en pesos colombianos (COP).
- El precio mostrado es de referencia; se revalida en el checkout.
- La paginación tiene un tamaño por defecto y un máximo.
- No se requiere sesión para explorar.

## Datos y servicios involucrados

- **Servicio:** `catalog-service`.
- **Base de datos:** `catalog_db`.
- **Entidades:** `products`, `product_variants`, `brands`, `categories`.

## Seguridad

- Endpoint público con límite de peticiones.
- No se exponen costos internos, márgenes ni campos de auditoría.
- Las consultas usan paginación para evitar respuestas enormes.

## Criterios de aceptación

- [ ] Un visitante ve el catálogo sin iniciar sesión.
- [ ] Solo aparecen productos activos.
- [ ] Cada tarjeta muestra marca, nombre, precio y disponibilidad.
- [ ] La paginación funciona y respeta el tamaño máximo.
- [ ] Un catálogo vacío muestra un estado claro, no un error.
