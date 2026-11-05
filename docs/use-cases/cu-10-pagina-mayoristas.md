# CU-10 — Ver página de mayoristas

| Campo | Valor |
|---|---|
| Módulo | Catálogo |
| Actores | Visitante y Cliente (principal) |
| Prioridad | Should |
| Diagrama | — |

## Objetivo

Informar que la venta al por mayor existirá más adelante, sin habilitar todavía un flujo B2B.

## Precondiciones

- Ninguna.

## Disparador

El usuario selecciona **Mayoristas** en el menú.

## Flujo principal

1. El frontend abre la página de mayoristas.
2. Muestra el mensaje **"Próximamente"**.
3. Explica brevemente qué ofrecerá el programa y qué requisitos tendrá.
4. Invita a volver al catálogo normal.

## Flujos alternativos

### A1 — Enlace directo sin sesión

- **Cuándo ocurre:** un visitante entra por URL.
- **Respuesta del sistema:** la página carga igual porque es pública.

## Postcondiciones

- El usuario conoce el estado futuro del programa de mayoristas.

## Reglas de negocio

- No hay formulario de registro B2B ni captura de datos.
- No se muestran listas de precios ni descuentos.
- La página es informativa y no altera el catálogo.

## Datos y servicios involucrados

- **Servicio:** ninguno; es una página estática del frontend.
- **Base de datos:** ninguna.

## Seguridad

- No se solicitan datos personales.
- No se enlazan recursos con derechos de autor sin autorización.

## Criterios de aceptación

- [ ] La página muestra claramente "Próximamente".
- [ ] No existe ningún flujo de compra mayorista.
- [ ] La página es accesible sin iniciar sesión.
