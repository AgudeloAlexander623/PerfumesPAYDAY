# Bitácora del backend

**Fecha:** 2026-11-13

## Resumen del día

Durante el día se completó la capa de autenticación JWT del backend. En Node.js se creó el módulo compartido de validación RS256 con claims (sub, iss, aud, exp, iat, jti y roles), guards de autenticación y rol, y configuración por entorno con fallo cerrado. El gateway quedó operativo con proxy /api/v1, CORS con orígenes explícitos y rechazo del comodín, rate limit global y estricto para auth, timeout, respuestas 503 con envelope, propagación de x-request-id y limpieza de cabeceras internas. Se añadieron 47 pruebas y la cobertura quedó en 73,09 %. En Python/FastAPI se construyó security-service: carga de clave RSA, firma RS256, JWKS, /health, envelope de errores, Dockerfile y servicio en Docker Compose. Se añadieron 20 pruebas. La integración extremo a extremo quedó verificada: el emisor generó un token, el gateway lo validó por JWKS y lo proxificó; sin token respondió 401. También se actualizó la bitácora y se realizaron cambios en el rol de PO (Product Owner) del proyecto.

## Cambios en el rol de PO

- Se realizaron cambios en el rol de PO (Product Owner) del proyecto.
