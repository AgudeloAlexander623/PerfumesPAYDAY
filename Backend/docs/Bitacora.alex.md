# Bitácora del backend

**Fecha:** 2026-11-20

## Resumen del día

Hoy construimos la base de la parte de seguridad de la aplicación. Preparamos un lugar propio y ordenado para guardar quiénes son los usuarios y cuándo comienza y termina cada visita. Antes esa idea vivía solo en los apuntes; ahora está instalada y funcionando.
¿Por qué lo hicimos? Porque para que una persona pueda registrarse y volver a entrar sin problemas, el sistema necesita recordarla y también cuidar ese recuerdo. Así evitamos que tenga que escribir su contraseña a cada momento y preparamos el terreno para que, más adelante, cerrar sesión signifique cerrarla de verdad. También pusimos al día los apuntes del equipo para que todos veamos el avance real y no una descripción antigua.
En el camino aparecieron tres detalles pequeños que corregimos con calma, y al final comprobamos que todo quedara bien: 24 revisiones salieron correctamente. Todavía falta crear los botones de registro e inicio de sesión, pero hoy dejamos unos cimientos claros, limpios y fáciles de seguir construyendo.

## cambios en el Rol de PO

**Fecha:** 2026-11-20
hicimos la primera daily para poder ver los avances dentro del proyecto, angel y daniel an habanzado en las tareas que ese les assignaron el dia lunes, a su ves se estan cumpliendo las metas del Sprint-GOAL para el dia Domingo realizaremos una vista previa para ver si realizamos parte del Sprint-backlog y ver que podemos mejorar para el dia lunes que es el dia de la sprint-planing de la segun semana

tambien hablamos con el scrum para poder ver si empezamos con la realizacion del Front para poder empezar con la creacion y coneccion de las API's que manejara el proyecto, ya que estas las tenemos que desarrollar desde cero para poder implementar el tema de los microservicios aparte de eso para poder conectarla como debe de ser con la aotomatizacion del proyecto
  

## 2026-11-13 — Capa JWT del backend

**Fecha:** 2026-11-13

## Resumen del día

Durante el día se completó la capa de autenticación JWT del backend. En Node.js se creó el módulo compartido de validación RS256 con claims (sub, iss, aud, exp, iat, jti y roles), guards de autenticación y rol, y configuración por entorno con fallo cerrado. El gateway quedó operativo con proxy /api/v1, CORS con orígenes explícitos y rechazo del comodín, rate limit global y estricto para auth, timeout, respuestas 503 con envelope, propagación de x-request-id y limpieza de cabeceras internas. Se añadieron 47 pruebas y la cobertura quedó en 73,09 %. En Python/FastAPI se construyó security-service: carga de clave RSA, firma RS256, JWKS, /health, envelope de errores, Dockerfile y servicio en Docker Compose. Se añadieron 20 pruebas. La integración extremo a extremo quedó verificada: el emisor generó un token, el gateway lo validó por JWKS y lo proxificó; sin token respondió 401. También se actualizó la bitácora y se realizaron cambios en el rol de PO (Product Owner) del proyecto.

## Cambios en el rol de PO

**Fecha:** 2026-11-13
Se realizaron cambios en el rol de PO (Product Owner) del proyecto.

