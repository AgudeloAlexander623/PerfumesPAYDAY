# Seguridad del sistema

Documento de amenazas, controles y pruebas de seguridad de **PerfumesPAYDAY**. Aplica a la beta académica y a todos los componentes: frontend, gateway, `security-service`, `catalog-service`, `order-service` y bases de datos.

> **Alcance:** simulador académico. No se manejan pagos reales, datos de tarjetas, facturación electrónica ni envíos reales. Los controles descritos son obligatorios para la beta y se verifican en las pruebas de hacking ético del profesor.

---

## 1. Principios

- **Seguridad desde el diseño:** no se agrega al final.
- **Defensa en profundidad:** el gateway valida, pero cada servicio vuelve a validar.
- **Mínimo privilegio:** cada servicio accede solo a su base de datos y a los recursos que necesita.
- **No confiar en el cliente:** el rol, el `user_id`, los precios y el stock salen del servidor.
- **Fallo seguro:** ante una duda, se deniega el acceso y se responde con un error genérico.
- **Datos mínimos:** no se registran contraseñas, tokens, datos de tarjetas ni datos personales innecesarios.
- **Trazabilidad:** las acciones administrativas quedan auditadas.

---

## 2. Activos y actores

### Activos

| Activo | Dónde vive | Por qué importa |
|---|---|---|
| Contraseñas | `security_db` (hash) | Compromiso de cuentas. |
| Access y refresh tokens | Cliente y `security_db` (hash del refresh) | Suplantación de identidad. |
| Datos personales | `security_db`, `orders_db` | Privacidad de usuarios. |
| Direcciones de envío | `orders_db` | Datos personales y de ubicación. |
| Pedidos e historial | `orders_db` | Información comercial y de clientes. |
| Catálogo, precios y stock | `catalog_db` | Integridad del negocio. |
| Auditoría | `catalog_db`, `orders_db` | No repudio de acciones administrativas. |
| Secretos de configuración | Entorno / archivos montados | Acceso a servicios y bases de datos. |

### Actores y roles

| Actor | Rol | Puede iniciar sesión |
|---|---|---|
| Visitante | Sin rol | No |
| Cliente | `customer` | Sí |
| Administrador | `admin` | Sí |
| Sistema | Servicios internos | No aplica |

> El rol **nunca** lo elige el usuario. El registro siempre crea `customer`; `admin` se asigna por fuera de la aplicación.

---

## 3. Modelo de amenazas

| Amenaza | Ejemplo | Control | Caso de uso |
|---|---|---|---|
| **Suplantación** | Robo de token o credenciales | JWT RS256, refresh rotado, cookies `httpOnly`, rate limit, Argon2/bcrypt | CU-02, CU-03 |
| **Manipulación** | Cliente envía precio, rol o `user_id` falsos | El servidor ignora esos campos y recalcula; rol y `user_id` salen del token | CU-06, CU-11, CU-17 |
| **Repudio** | Administrador niega un cambio | Auditoría append-only con actor, acción, entidad, fecha, IP y agente | CU-23 |
| **Divulgación de información** | IDOR en pedidos o direcciones | Filtrar por `user_id` en la misma consulta; responder `404` ante recursos ajenos | CU-16, CU-19 |
| **Denegación de servicio** | Fuerza bruta o scraping | Rate limit por IP y por usuario; límite de tamaño de cuerpo | CU-01, CU-02, CU-07 |
| **Elevación de privilegios** | Cliente accede a rutas de administración | Validar rol `admin` en gateway y en el servicio | CU-20 a CU-25 |
| **Inyección** | SQL o XSS en búsqueda | Consultas parametrizadas/ORM; escapar al renderizar; validar tipos y rangos | CU-08 |
| **Exposición de secretos** | `.env` versionado o logs con tokens | `.gitignore`, `.env.example`, logs sin secretos, escaneo de dependencias | Transversal |
| **CSRF** | Petición maliciosa con cookie de refresh | `SameSite`, validación de `Origin` en el gateway | CU-02, CU-03 |
| **Dependencias comprometidas** | Paquete malicioso | Versiones bloqueadas, lockfile, revisión de dependencias | Transversal |

---

## 4. Autenticación

### Registro

- Validar nombre, correo y contraseña en el servidor con Pydantic.
- Correo único, guardado en minúsculas.
- Contraseña con Argon2 o bcrypt; nunca cifrado reversible.
- Rol `customer` asignado por el servidor.
- Respuesta sin `password_hash` ni datos internos.
- Límite de intentos por IP y por correo.

### Inicio de sesión

- Comparación de contraseña en tiempo constante.
- Mensaje genérico `401` para correo inexistente o contraseña incorrecta.
- Emitir access token de corta duración y refresh token de varios días.
- Guardar solo el hash del refresh token en `security_db`.
- Registrar `user_agent`, `ip`, `created_at` y `expires_at` de la sesión.
- Reiniciar el contador de intentos fallidos tras un login exitoso.

### Renovación

- El refresh token viaja en cookie `httpOnly`, `Secure` y `SameSite`.
- Rotación obligatoria en cada uso.
- Reutilizar un refresh ya rotado revoca todas las sesiones del usuario.
- La sesión tiene una vida absoluta aunque se renueve.
- El gateway valida el origen para prevenir CSRF.

### Cierre de sesión

- Revocar la sesión actual por el refresh token.
- Eliminar la cookie.
- Responder `204` aunque no haya sesión activa (idempotente).
- Ofrecer cierre de todas las sesiones desde el perfil.
- No eliminar carrito ni historial.

### Almacenamiento en el cliente

- Access token en memoria; no en `localStorage`.
- Refresh token en cookie `httpOnly`; no accesible por JavaScript.
- El carrito de invitado guarda solo `variant_id` y cantidad, nunca precios.
- Si el equipo cambia esta estrategia, debe registrarlo en un ADR.

**Decisión abierta:** la entrega de la clave pública JWT está en [ADR-0003](adr/0003-jwt-rs256.md).

---

## 5. Autorización y RBAC

| Recurso / acción | Visitante | Cliente (`customer`) | Administrador (`admin`) |
|---|---|---|---|
| Catálogo público (CU-07 a CU-10) | Permitido | Permitido | Permitido |
| Registro, login, refresh (CU-01 a CU-03) | Permitido | Permitido | Permitido |
| Logout (CU-04) | Permitido si hay cookie | Permitido | Permitido |
| Perfil propio (CU-05, CU-06, CU-24) | `401` | Solo el propio | Solo el propio |
| Carrito propio (CU-11 a CU-15) | `401` en backend; carrito local | Solo el propio | Solo el propio |
| Direcciones propias (CU-16) | `401` | Solo las propias | Solo las propias |
| Checkout y pedidos propios (CU-17 a CU-19) | `401` | Solo los propios | Solo los propios |
| Productos y stock (CU-20) | `403` | `403` | Permitido |
| Pedidos de todos los clientes (CU-21, CU-22) | `403` | `403` | Permitido |
| Auditoría (CU-23) | `403` | `403` | Permitido |
| Marcas y categorías (CU-25) | `403` | `403` | Permitido |

Reglas:

- El gateway valida el token y el rol; el servicio vuelve a validar.
- Un cliente que intenta una ruta de administración recibe `403`.
- Un recurso ajeno responde `404`, no `403`, para no confirmar su existencia.
- El `user_id` se obtiene del token, nunca de un parámetro.
- El rol se lee de la base de datos, no del token, cuando la operación es sensible.

---

## 6. IDOR y propiedad de recursos

- Toda consulta de carrito, dirección, pedido o perfil filtra por `user_id` en la misma consulta a la base de datos.
- No se filtra en memoria después de traer el registro.
- Si el recurso no pertenece al usuario, se responde `404`.
- El administrador puede consultar pedidos de todos, pero no modificar datos personales fuera de su alcance.
- La auditoría registra el actor real de cada acción administrativa.

Casos críticos: CU-16 (direcciones), CU-19 (detalle de pedido), CU-21 y CU-22 (administración).

---

## 7. Validación y sanitización

- **Backend:** Zod en Node.js y Pydantic en Python; nunca confiar en la validación del frontend.
- **Tipos:** validar UUID, enteros, rangos de precio y stock, longitudes y formatos.
- **SQL:** consultas parametrizadas u ORM; nunca concatenar SQL.
- **XSS:** escapar el texto al renderizar; no usar `dangerouslySetInnerHTML` con datos del usuario.
- **Imágenes:** referenciar por URL validada; no permitir subida de archivos ejecutables.
- **Listas blancas:** en edición de perfil solo se acepta `name`; `email`, `role` e `id` se ignoran.
- **Cuerpo de la petición:** límite de tamaño y rechazo de campos desconocidos cuando aplique.
- **Respuestas:** no incluir `password_hash`, tokens, costos internos, márgenes ni notas internas.

---

## 8. Transporte, cabeceras y CORS

- HTTPS obligatorio en producción; el gateway es el único punto público.
- Helmet en el gateway y en los servicios Node.js.
- CORS con lista explícita de orígenes permitidos; no usar `*` con credenciales.
- Cabeceras recomendadas: `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options` o `frame-ancestors`.
- Cookies de refresh con `httpOnly`, `Secure` y `SameSite`.
- Validar `Origin` en operaciones con cookies para prevenir CSRF.
- No exponer PostgreSQL ni los servicios internos a internet.
- Contenedores con usuario sin privilegios.

---

## 9. Rate limiting y abuso

| Operación | Límite propuesto | Nota |
|---|---|---|
| Registro | Por IP y por correo | Evita creación masiva de cuentas. |
| Login | Por cuenta y por IP | Protege fuerza bruta. |
| Refresh | Por sesión | Evita abuso de rotación. |
| Catálogo y búsqueda | Por IP | Evita scraping. |
| Carrito y checkout | Por usuario | Evita abuso de stock. |
| Administración | Por usuario | Protege cargas masivas. |

- El almacén en memoria sirve para una instancia; si se escala, se requiere Redis u otro almacén externo.
- Responder `429` con tiempo de espera.
- El rate limit no reemplaza la autorización ni la validación.

---

## 10. Secretos y configuración

- Los secretos viven en variables de entorno o archivos montados; nunca en el repositorio.
- Solo se versiona `.env.example` con valores ficticios.
- `.gitignore` excluye `.env` y `.env.*`.
- No se registran secretos en logs, errores ni respuestas.
- Rotar credenciales si se exponen.
- Cada servicio usa credenciales propias de su base de datos.
- La clave privada JWT solo la conoce `security-service`; el backend solo recibe la pública.

---

## 11. Logs, auditoría y privacidad

### Logs

- Formato JSON estructurado.
- Incluir `requestId`, servicio, ruta, método, estado y duración.
- No incluir contraseñas, tokens, cookies, `password_hash` ni datos personales completos.
- No registrar el cuerpo completo de las peticiones.
- Nivel de log configurable por entorno.

### Auditoría

- Cada servicio escribe en su propia tabla `audit_events`.
- La escritura ocurre en la misma transacción que la acción administrativa.
- Si falla la auditoría, la acción se revierte y se responde `503` (CU-23).
- Campos mínimos: actor, acción, entidad, identificador, resumen del cambio, fecha, IP y agente.
- La auditoría es append-only; no se edita ni se elimina desde la aplicación.
- El administrador consulta la auditoría; el gateway agrega los resultados de `catalog` y `orders`.

### Privacidad

- Minimización de datos: la lista de pedidos del administrador muestra nombre y correo, no la dirección completa.
- Los datos personales no se usan para analítica ni marketing.
- La eliminación de una dirección no altera los pedidos históricos porque el pedido guarda su propia copia.

---

## 12. Dependencias y cadena de suministro

- Versiones bloqueadas con `package-lock.json`.
- Revisar dependencias antes de agregarlas; evitar paquetes sin mantenimiento.
- Ejecutar `npm audit` y el equivalente de Python cuando exista CI.
- No instalar dependencias de base de datos o frontend en el backend sin autorización.
- Revisar que los plugins de Fastify sean oficiales o estén bien mantenidos.
- No ejecutar contenedores como `root`.

---

## 13. Pruebas de hacking ético

El profesor realizará pruebas básicas sobre la versión desplegada. El equipo debe preparar evidencia y correcciones en este documento.

| Prueba | Qué se verifica | Evidencia |
|---|---|---|
| Autenticación | Login inválido, cuenta deshabilitada, expiración y refresh | Capturas y resultados de pruebas. |
| Autorización | Cliente en rutas de administración | `403` esperado. |
| IDOR | Pedido, dirección y carrito de otro usuario | `404` esperado. |
| Inyección SQL | Búsqueda con caracteres especiales | Consulta parametrizada; sin error 500. |
| XSS | Texto malicioso en búsqueda o perfil | Se muestra escapado. |
| CORS | Origen no permitido | Sin cabecera de permiso. |
| Rate limit | Ráfaga de login o búsqueda | `429` esperado. |
| Secretos | Repositorio y logs | Sin `.env`, tokens ni contraseñas. |
| Escaneo | OWASP ZAP básico | Reporte y correcciones. |
| Dependencias | `npm audit` / Python | Sin vulnerabilidades críticas sin tratar. |

### Checklist mínimo antes de la demo

- [ ] HTTPS y cabeceras de seguridad activas.
- [ ] CORS restringido a los orígenes reales.
- [ ] Rate limit en login, registro y checkout.
- [ ] Contraseñas con hash y sin exposición.
- [ ] Tokens fuera de logs y de `localStorage`.
- [ ] Rutas de administración protegidas en gateway y servicio.
- [ ] Consultas filtradas por `user_id`.
- [ ] Errores genéricos en autenticación y recursos ajenos.
- [ ] Auditoría de acciones administrativas.
- [ ] `.env.example` sin secretos reales.
- [ ] Contenedores sin privilegios.
- [ ] Resultados de OWASP ZAP documentados.

---

## 14. Respuesta a incidentes

1. Detectar y registrar el incidente sin exponer datos sensibles.
2. Revocar sesiones y rotar credenciales afectadas.
3. Revisar logs y auditoría con el `requestId`.
4. Corregir la causa y agregar una prueba de regresión.
5. Documentar el incidente y la corrección en este archivo.
6. Informar al equipo y, si aplica, al profesor.

---

## 15. Decisiones abiertas

| Decisión | Impacto | ADR |
|---|---|---|
| Entrega de la clave pública JWT | Autenticación y despliegue | [ADR-0003](adr/0003-jwt-rs256.md) |
| Contrato backend–BD | Acceso a datos y credenciales | [ADR-0004](adr/0004-propiedad-datos.md) |
| Comunicación interna | Autenticación entre servicios | [ADR-0005](adr/0005-comunicacion-interna.md) |
| Formato de errores | Evitar filtrar información interna | [ADR-0006](adr/0006-errores-paginacion-idempotencia.md) |

---

## 16. Referencias

- [Arquitectura](architecture.md)
- [Casos de uso](use-cases/README.md)
- [API](api/README.md)
- [ADR](adr/README.md)
- [README raíz](../README.md)
- [Plan del backend](PLAN.md)

---

**Última actualización:** 2026-11-10
**Estado:** redactado; sujeto a las decisiones abiertas de los ADR.
