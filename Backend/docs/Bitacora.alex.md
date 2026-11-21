# Bitácora del backend

**Fecha:** 2026-11-20

## Resumen del día

Se creó la base de datos del servicio de seguridad para poder guardar usuarios y sesiones, algo necesario para iniciar sesión y renovar tokens. Se definieron las tablas `users` y `sessions`, se agregó PostgreSQL a Docker y se ajustó el gateway para validar los tokens con el JWKS. También se actualizó la documentación para que el equipo vea el avance real del proyecto. Después de corregir tres fallos durante las pruebas, quedaron 24 pruebas de Python en verde.
