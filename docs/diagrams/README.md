# Diagramas del proyecto

Diagramas de arquitectura y flujo en formato SVG. Cada diagrama tiene dos archivos:

- `.mmd`: fuente editable en Mermaid.
- `.svg`: versión final para abrir en cualquier IDE, navegador o GitHub.

## Índice

| # | Diagrama | Fuente | SVG | Qué explica |
|---|---|---|---|---|
| 01 | Contexto del sistema | [`01-contexto-sistema.mmd`](01-contexto-sistema.mmd) | [`01-contexto-sistema.svg`](01-contexto-sistema.svg) | Actores, red pública, servicios internos y bases de datos |
| 02 | Arquitectura de contenedores | [`02-arquitectura-contenedores.mmd`](02-arquitectura-contenedores.mmd) | [`02-arquitectura-contenedores.svg`](02-arquitectura-contenedores.svg) | Comunicación entre servicios, protocolos y propiedad de los datos |
| 03 | Autenticación | [`03-autenticacion.mmd`](03-autenticacion.mmd) | [`03-autenticacion.svg`](03-autenticacion.svg) | Registro, login, tokens, renovación y cierre de sesión |
| 04 | Catálogo | [`04-catalogo.mmd`](04-catalogo.mmd) | [`04-catalogo.svg`](04-catalogo.svg) | Búsqueda, filtros, detalle, presentaciones y stock |
| 05 | Carrito por usuario | [`05-carrito-usuario.mmd`](05-carrito-usuario.mmd) | [`05-carrito-usuario.svg`](05-carrito-usuario.svg) | Carrito asociado al usuario y validación de stock |
| 06 | Direcciones y checkout | [`06-direcciones-checkout.mmd`](06-direcciones-checkout.mmd) | [`06-direcciones-checkout.svg`](06-direcciones-checkout.svg) | Dirección de envío, revalidación, pedido y pago simulado |
| 07 | Historial de pedidos | [`07-historial-pedidos.mmd`](07-historial-pedidos.mmd) | [`07-historial-pedidos.svg`](07-historial-pedidos.svg) | Consulta de pedidos y control de acceso por usuario |
| 08 | Administración | [`08-administracion.mmd`](08-administracion.mmd) | [`08-administracion.svg`](08-administracion.svg) | Validación de rol, gestión de productos y pedidos, auditoría |

## Leyenda

| Color o forma | Significado |
|---|---|
| Naranja | Usuario o actor externo |
| Azul | Frontend o paso del proceso |
| Cian | Gateway |
| Verde | Servicio interno o resultado exitoso |
| Morado | Base de datos |
| Amarillo | Decisión |
| Rojo | Error o acceso denegado |
| Gris | Inicio, fin o elemento futuro |
| Rombo | Pregunta o decisión |
| Cilindro | Base de datos |

## Cómo leer los diagramas

- Los diagramas **01 y 02** muestran la arquitectura general.
- Los diagramas **03 a 08** muestran flujos de uso.
- Las flechas indican el orden de las acciones.
- Las etiquetas sobre las flechas indican condiciones o datos que se envían.
- El diagrama **03** usa un diagrama de secuencia porque el login implica varios actores intercambiando mensajes.

## Mantenimiento

- Editar siempre el archivo `.mmd`, no el `.svg`.
- Regenerar el SVG después de cada cambio.
- Mantener el mismo estilo, colores y nombres en todos los diagramas.
- Si un flujo cambia, actualizar también el README o la documentación relacionada.

Comando de referencia para regenerar un diagrama:

```bash
npx @mermaid-js/mermaid-cli -i archivo.mmd -o archivo.svg -b white
```
