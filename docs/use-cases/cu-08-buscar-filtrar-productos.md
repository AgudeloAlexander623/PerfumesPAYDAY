# CU-08 — Buscar y filtrar productos

| Campo | Valor |
|---|---|
| Módulo | Catálogo |
| Actores | Visitante y Cliente (principal) |
| Prioridad | Must |
| Diagrama | [`04-catalogo`](../diagrams/04-catalogo.svg) |

## Objetivo

Permitir que el usuario encuentre perfumes por texto, marca, género, familia olfativa y rango de precio.

## Precondiciones

- Ninguna. La búsqueda es pública.

## Disparador

El usuario escribe en el buscador o selecciona uno o más filtros.

## Flujo principal

1. El usuario escribe un término o selecciona filtros.
2. El frontend espera un breve momento para no enviar una petición por cada tecla.
3. Envía la búsqueda al gateway con los filtros activos.
4. El gateway la enruta a `catalog-service`.
5. `catalog-service` construye una consulta parametrizada y la ejecuta en `catalog_db`.
6. Devuelve los productos que cumplen **todos** los filtros, junto con el total de resultados.
7. El frontend actualiza la lista y guarda los filtros en la URL para poder compartirla o recargar sin perderla.

## Flujos alternativos

### A1 — Sin resultados

- **Cuándo ocurre:** ningún producto cumple los filtros.
- **Respuesta del sistema:** muestra un estado vacío y un botón para limpiar los filtros.

### A2 — Filtro inválido

- **Cuándo ocurre:** el precio mínimo es mayor que el máximo o el género no existe.
- **Respuesta del sistema:** responde `400` con el filtro a corregir; el frontend no aplica el cambio.

### A3 — Intento de inyección

- **Cuándo ocurre:** el término contiene caracteres especiales de SQL o HTML.
- **Respuesta del sistema:** la consulta parametrizada los trata como texto y el frontend los escapa al mostrarlos.

### A4 — Servicio no disponible

- **Cuándo ocurre:** `catalog-service` no responde.
- **Respuesta del sistema:** responde `503` y conserva los filtros para reintentar.

## Postcondiciones

- El usuario ve los resultados que cumplen los filtros y puede limpiarlos.

## Reglas de negocio

- La búsqueda por texto es parcial y no distingue mayúsculas de minúsculas.
- Los filtros se combinan con **Y**, no con **O**.
- El orden puede ser por relevancia, precio ascendente, precio descendente o novedad.
- El término de búsqueda tiene una longitud máxima.
- Los filtros viven en la URL para que la página sea reproducible.

## Datos y servicios involucrados

- **Servicio:** `catalog-service`.
- **Base de datos:** `catalog_db`.
- **Entidades:** `products`, `product_variants`, `brands`, `categories`.

## Seguridad

- Consultas parametrizadas o mediante ORM; nunca SQL concatenado.
- Límite de peticiones para evitar abuso del buscador.
- Validación del tipo y rango de cada filtro en el servidor.
- El texto se escapa al renderizar para prevenir XSS.

## Criterios de aceptación

- [ ] La búsqueda por nombre o marca devuelve resultados parciales.
- [ ] Los filtros se pueden combinar y se reflejan en la URL.
- [ ] Un filtro inválido devuelve `400`.
- [ ] Un término con caracteres especiales no rompe la consulta.
- [ ] Sin resultados se muestra un estado vacío con opción de limpiar.
