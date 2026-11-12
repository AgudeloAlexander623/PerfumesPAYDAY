# Criterios de aceptación de la beta — PerfumesPAYDAY

> **Estado:** redactado — pendiente de validación con el equipo y el profesor.
> **Última actualización:** 2026-11-11
> **Fuente de verdad:** el comportamiento funcional vive en [`use-cases/`](use-cases/README.md) y las historias en [`user-stories/`](user-stories/user-stories.md). Este documento no los repite: los convierte en **criterios verificables** y en el **guion de demo**.
> **Propósito:** ser el contrato de aceptación de la beta. Cuando todos los criterios de la sección 4 estén en verde, la beta se considera terminada.

---

## 1. Para qué sirve este documento

El README (sección 14) resume qué debe tener la beta; este documento lo vuelve **verificable**: cada criterio dice **qué** se comprueba, **cómo** se comprueba y **con qué evidencia**. Sirve para tres cosas:

1. **Cerrar el alcance.** Solo cuenta lo que se puede demostrar.
2. **Guiar la demo.** El guion de la sección 9 recorre la beta de punta a punta.
3. **Definir el go/no-go.** La sección 10 explica cuándo se declara lista.

Un criterio está **cumplido** cuando su evidencia existe y es reproducible por otra persona.

---

## 2. Definición de "beta lista"

La beta está lista cuando se cumplen **las cinco condiciones** a la vez:

1. **Funcional:** los 18 casos de uso **Must** pasan sus criterios (sección 4).
2. **Segura:** la prueba de hacking ético no deja hallazgos **críticos ni altos** abiertos (sección 5).
3. **Desplegada:** está en una **URL pública con HTTPS** y `docker-compose` levanta el entorno local (sección 7).
4. **Documentada:** la documentación por componente está actualizada (sección 6).
5. **Demostrable:** el guion de la sección 9 se ejecuta sin fallos de principio a fin.

Si alguna falla, la beta **no** se declara lista, aunque haya funcionalidades extra terminadas.

---

## 3. Alcance

### 3.1 Dentro de la beta

- Los **18 casos de uso Must** y las historias asociadas.
- Las historias **Should/Could** que el equipo logre cerrar (no bloquean la aceptación, pero suman).
- Catálogo con 25 a 30 productos simulados, presentaciones de 30, 50 y 100 ml.
- Diseño responsive con estados de carga y error.

### 3.2 Fuera de la beta

Pasarelas de pago reales, facturación electrónica DIAN, envíos reales o cálculo con transportadoras, aplicación móvil nativa, flujo B2B completo, inventario multibodega, reseñas, wishlist, fidelización, analítica avanzada, recuperación de contraseña por correo, verificación de correo, cancelación de pedidos, cupones y gestión de usuarios/roles desde el panel.

> Ningún criterio de esta lista se evalúa en la beta. Si aparece una funcionalidad fuera de alcance, se rechaza y se registra para una fase posterior.

---

## 4. Criterios funcionales (los 18 Must)

Cada criterio se marca `[ ]` al verificarse. La columna **Evidencia** indica qué se adjunta para demostrarlo.

### 4.1 Cuentas y sesión

| ID | Criterio de aceptación | Caso de uso | Evidencia |
|---|---|---|---|
| B-01 | Un visitante puede registrarse con datos válidos y su cuenta se crea con rol `cliente`. | CU-01 | Video/captura + respuesta de API |
| B-02 | Un correo ya registrado no crea una cuenta duplicada y muestra un mensaje claro. | CU-01 | Captura + prueba automática |
| B-03 | Un usuario con credenciales correctas inicia sesión y recibe token de acceso y refresh token. | CU-02 | Respuesta de API |
| B-04 | Credenciales incorrectas devuelven un mensaje genérico que no revela qué dato falló. | CU-02 | Captura |
| B-05 | Superar el límite de intentos de login/registro devuelve `429`. | CU-01, CU-02 | Prueba automática |
| B-06 | El token de acceso se renueva con el refresh token sin interrumpir al usuario. | CU-03 | Prueba automática |
| B-07 | Cerrar sesión revoca el refresh token y devuelve al estado de visitante. | CU-04 | Prueba automática |

### 4.2 Catálogo

| ID | Criterio de aceptación | Caso de uso | Evidencia |
|---|---|---|---|
| B-08 | El catálogo muestra los productos con nombre, marca y precio en COP, visible para visitantes. | CU-07 | Captura |
| B-09 | La búsqueda y los filtros (marca, género, familia olfativa) devuelven solo los productos que cumplen. | CU-08 | Captura + prueba |
| B-10 | El detalle muestra marca, género, familia, presentaciones, precio y stock por presentación. | CU-09 | Captura |
| B-11 | Una presentación sin stock se muestra agotada y no se puede agregar al carrito. | CU-09 | Captura |
| B-12 | Un producto inexistente muestra "producto no encontrado". | CU-09 | Captura |

### 4.3 Carrito

| ID | Criterio de aceptación | Caso de uso | Evidencia |
|---|---|---|---|
| B-13 | Un visitante agrega productos y los conserva durante su sesión (carrito híbrido). | CU-11 | Captura |
| B-14 | Un cliente autenticado guarda su carrito en el servidor, asociado a su `user_id`. | CU-11 | Respuesta de API |
| B-15 | No se puede agregar ni actualizar una cantidad mayor al stock disponible. | CU-11, CU-13 | Prueba automática |
| B-16 | El carrito muestra ítems, cantidades, precios vigentes y total recalculado en el servidor. | CU-12 | Captura |
| B-17 | Eliminar un ítem o dejarlo en cero lo quita del carrito y actualiza el total. | CU-13, CU-14 | Captura |
| B-18 | Al iniciar sesión, el carrito de invitado se fusiona con el del usuario sin perder ítems. | CU-15 | Video |
| B-19 | La fusión no duplica líneas ni cantidades y respeta el stock. | CU-15 | Prueba automática |

### 4.4 Checkout y direcciones

| ID | Criterio de aceptación | Caso de uso | Evidencia |
|---|---|---|---|
| B-20 | Un cliente crea, lista, edita y elimina sus direcciones; la primera queda predeterminada. | CU-16 | Captura |
| B-21 | Solo existe una dirección predeterminada por usuario. | CU-16 | Prueba automática |
| B-22 | Un cliente puede confirmar la compra y se crea un pedido con copia de productos, precios y dirección. | CU-17 | Video + respuesta de API |
| B-23 | El total del pedido se calcula en el servidor; no se confía en montos del navegador. | CU-17 | Prueba automática |
| B-24 | Un cambio de precio o de stock bloquea la compra con `409` y no crea el pedido. | CU-17 | Prueba automática |
| B-25 | Reintentar la compra (doble clic o repetición de red) no duplica el pedido (idempotencia). | CU-17 | Prueba automática |
| B-26 | El pago queda marcado como simulado; no se pide ni se almacena ningún dato de tarjeta. | CU-17 | Revisión de código |

### 4.5 Pedidos

| ID | Criterio de aceptación | Caso de uso | Evidencia |
|---|---|---|---|
| B-27 | El cliente ve solo sus pedidos, del más reciente al más antiguo, con su estado. | CU-18 | Captura |
| B-28 | El detalle del pedido muestra el snapshot (nombre, presentación y precio del momento). | CU-19 | Captura |
| B-29 | Acceder al pedido de otra persona devuelve `404` (IDOR). | CU-19 | Prueba automática |

### 4.6 Administración

| ID | Criterio de aceptación | Caso de uso | Evidencia |
|---|---|---|---|
| B-30 | Un `admin` crea, edita y desactiva productos y presentaciones con validación en el servidor. | CU-20 | Captura |
| B-31 | Un `cliente` recibe `403` al intentar una acción de administración. | CU-20, CU-21 | Prueba automática |
| B-32 | El `admin` consulta los pedidos de todos los clientes y su detalle. | CU-21 | Captura |
| B-33 | El panel administrativo está protegido y solo accesible con rol `admin`. | CU-20, CU-21 | Captura |

---

## 5. Criterios de seguridad (hacking ético)

El profesor probará estos puntos sobre la versión desplegada (README, sección 10). Los resultados y correcciones se documentan en [`security.md`](security.md).

| ID | Prueba | Resultado esperado | Evidencia |
|---|---|---|---|
| S-01 | Acceso a una ruta protegida sin token | Redirección a login o `401` | Captura |
| S-02 | `cliente` llamando a un endpoint de administración | `403` | Prueba |
| S-03 | IDOR: cambiar el ID por el de un pedido o dirección ajena | `404` | Prueba |
| S-04 | Inyección SQL en búsqueda y filtros | Sin efecto; consultas parametrizadas | Prueba |
| S-05 | XSS en campos de texto y búsqueda | El texto se escapa; no se ejecuta | Prueba |
| S-06 | CORS | Solo orígenes permitidos; servicios internos no expuestos | Revisión |
| S-07 | Rate limit en login, registro y checkout | Bloqueo temporal (`429`) | Prueba |
| S-08 | Secretos expuestos | Sin claves ni `.env` en el repositorio | Revisión |
| S-09 | Escaneo con OWASP ZAP | Sin hallazgos altos o críticos abiertos | Reporte |
| S-10 | Contraseñas en reposo | Guardadas con Argon2 o bcrypt | Revisión |

---

## 6. Criterios de calidad transversal

| ID | Criterio | Evidencia |
|---|---|---|
| Q-01 | La interfaz es usable en celular, tablet y computador, sin desplazamiento horizontal. | Capturas en 3 tamaños |
| Q-02 | Hay estados de carga y de error claros; los errores no exponen detalles internos. | Captura |
| Q-03 | Las fechas usan ISO 8601 UTC y los precios COP con IVA incluido. | Revisión |
| Q-04 | Los identificadores son UUID. | Revisión |
| Q-05 | La documentación de cada componente está actualizada. | Enlaces en `docs/` |
| Q-06 | La integración continua pasa (lint y pruebas). | Estado del pipeline |

---

## 7. Criterios de infraestructura y despliegue

| ID | Criterio | Evidencia |
|---|---|---|
| I-01 | La beta está en una **URL pública con HTTPS**. | Enlace funcionando |
| I-02 | `docker-compose` levanta servicios y bases de datos con un solo comando. | Guía reproducible |
| I-03 | El *seed* carga los 25 a 30 productos de forma idempotente. | Ejecución doble |
| I-04 | Solo el gateway es accesible desde internet; los servicios internos y PostgreSQL no. | Revisión |
| I-05 | Los contenedores se ejecutan con un usuario sin privilegios. | Revisión |

---

## 8. Registro de evidencia

Cada criterio se cierra adjuntando su evidencia en la tarjeta del tablero. Tabla de seguimiento:

| Bloque | Total | Cumplidos | Pendientes |
|---|---|---|---|
| Funcional (B-01 a B-33) | 33 | | |
| Seguridad (S-01 a S-10) | 10 | | |
| Calidad (Q-01 a Q-06) | 6 | | |
| Infraestructura (I-01 a I-05) | 5 | | |

> La evidencia puede ser un video corto, una captura, la respuesta de la API o una prueba automática. Sin evidencia, el criterio no se marca.

---

## 9. Guion de demo

Recorrido sugerido (10 a 15 minutos) para la revisión final. Se ejecuta sobre la URL desplegada.

1. **Presentación (1 min):** qué es PerfumesPAYDAY y que el pago es simulado.
2. **Catálogo (2 min):** explorar, buscar por marca y filtrar por género y familia olfativa.
3. **Detalle (1 min):** abrir un producto, cambiar de presentación y ver precio y stock.
4. **Carrito como visitante (1 min):** agregar sin sesión y ver el contador.
5. **Registro y fusión (2 min):** registrarse/iniciar sesión y mostrar que el carrito se conserva (CU-15).
6. **Direcciones (1 min):** crear una dirección y marcarla como predeterminada.
7. **Checkout (2 min):** confirmar la compra y mostrar la confirmación con el pago simulado.
8. **Pedidos (1 min):** ver el historial y el detalle con el snapshot.
9. **Administración (2 min):** entrar con rol `admin`, crear/editar un producto y consultar pedidos.
10. **Seguridad (1 min):** mostrar un intento de IDOR devolviendo `404` y un `403` de cliente.
11. **Cierre (1 min):** mostrar la URL, el repositorio y la documentación.

---

## 10. Criterios de go / no-go

**GO** — se declara la beta lista si:

- Todos los criterios funcionales Must (B-01 a B-33) están cumplidos.
- No hay hallazgos de seguridad **críticos ni altos** abiertos (sección 5).
- La URL pública con HTTPS responde (I-01) y `docker-compose` levanta (I-02).
- El guion de la sección 9 se ejecuta sin fallos.
- La documentación está actualizada (Q-05).

**NO-GO** — se aplaza si falla cualquiera de las condiciones anteriores, aunque haya funcionalidades extra.

> Las historias **Should/Could** que no se cierren **no** impiden el GO; se registran como trabajo futuro.

---

## 11. Aprobación

| Rol | Responsable | Fecha | Firma |
|---|---|---|---|
| Product Owner | | | |
| Líder técnico | | | |
| Profesor / evaluador | | | |

---

**Versión:** 0.1
**Responsable:** Product Owner
