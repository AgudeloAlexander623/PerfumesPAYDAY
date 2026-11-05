# Casos de uso

Un **caso de uso** describe una interacción completa entre un actor y el sistema para lograr un objetivo concreto. Sirve para acordar **qué debe hacer** la aplicación antes de decidir **cómo** se implementa.

Este catálogo es la base para planear el alcance de la beta, escribir los contratos de API y validar los diagramas de flujo.

---

## 1. Actores

| Actor | Descripción | Puede iniciar sesión |
|---|---|---|
| **Visitante** | Persona sin sesión iniciada que explora el catálogo | No |
| **Cliente** | Usuario registrado con rol `customer` | Sí |
| **Administrador** | Usuario con rol `admin` que gestiona catálogo y pedidos | Sí |
| **Sistema** | Servicios internos que ejecutan validaciones y tareas automáticas | No aplica |

> El rol **nunca** lo elige el usuario. El registro siempre crea un `customer`; el rol `admin` se asigna por fuera de la aplicación.

---

## 2. Catálogo de casos de uso

### Autenticación y cuenta

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| [CU-01](cu-01-registro.md) | Registrarse | Visitante | Must | 03 |
| [CU-02](cu-02-inicio-sesion.md) | Iniciar sesión | Visitante | Must | 03 |
| [CU-03](cu-03-renovar-sesion.md) | Renovar sesión | Cliente / Administrador | Must | 03 |
| [CU-04](cu-04-cerrar-sesion.md) | Cerrar sesión | Cliente / Administrador | Must | 03 |
| [CU-05](cu-05-consultar-perfil.md) | Consultar perfil | Cliente | Should | — |
| [CU-06](cu-06-editar-perfil.md) | Editar perfil | Cliente | Could | — |
| [CU-24](cu-24-cambiar-contrasena.md) | Cambiar contraseña | Cliente / Administrador | Should | — |

### Catálogo

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| [CU-07](cu-07-explorar-catalogo.md) | Explorar catálogo | Visitante / Cliente | Must | 04 |
| [CU-08](cu-08-buscar-filtrar-productos.md) | Buscar y filtrar productos | Visitante / Cliente | Must | 04 |
| [CU-09](cu-09-ver-detalle-producto.md) | Ver detalle de producto | Visitante / Cliente | Must | 04 |
| [CU-10](cu-10-pagina-mayoristas.md) | Ver página de mayoristas | Visitante / Cliente | Should | — |

### Carrito

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| [CU-11](cu-11-agregar-al-carrito.md) | Agregar producto al carrito | Cliente / Visitante | Must | 05 |
| [CU-12](cu-12-ver-carrito.md) | Ver carrito | Cliente / Visitante | Must | 05 |
| [CU-13](cu-13-actualizar-cantidad.md) | Actualizar cantidad | Cliente / Visitante | Must | 05 |
| [CU-14](cu-14-eliminar-del-carrito.md) | Eliminar producto del carrito | Cliente / Visitante | Must | 05 |
| [CU-15](cu-15-fusionar-carrito.md) | Fusionar carrito al iniciar sesión | Cliente | Must | 05 |

### Checkout y direcciones

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| [CU-16](cu-16-gestionar-direcciones.md) | Gestionar direcciones de envío | Cliente | Must | 06 |
| [CU-17](cu-17-checkout-simulado.md) | Realizar checkout simulado | Cliente | Must | 06 |

### Pedidos

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| [CU-18](cu-18-historial-pedidos.md) | Consultar historial de pedidos | Cliente | Must | 07 |
| [CU-19](cu-19-detalle-pedido.md) | Ver detalle de un pedido | Cliente | Must | 07 |

### Administración

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| [CU-20](cu-20-gestionar-productos.md) | Gestionar productos | Administrador | Must | 08 |
| [CU-21](cu-21-consultar-pedidos-admin.md) | Consultar pedidos | Administrador | Must | 08 |
| [CU-22](cu-22-revisar-estado-pedido.md) | Revisar estado de un pedido | Administrador | Should | 08 |
| [CU-23](cu-23-auditar-acciones.md) | Auditar acciones administrativas | Sistema / Administrador | Should | 08 |
| [CU-25](cu-25-gestionar-marcas-categorias.md) | Gestionar marcas y categorías | Administrador | Should | 08 |

**Total: 25 casos** — 18 Must, 6 Should y 1 Could.

### Nota de consolidación

El planteamiento inicial proponía 27 casos. Para evitar documentos redundantes se integraron dos:

- **"Cerrar sesión en todos los dispositivos"** quedó como flujo alternativo del CU-04.
- **"Consultar el registro de auditoría"** quedó dentro del CU-23, que cubre registro y consulta.

Así cada caso tiene un objetivo distinto y no se repite información.

---

## 3. Prioridades

Se usa la escala **MoSCoW**:

| Prioridad | Significado |
|---|---|
| **Must** | Obligatorio para que la beta se considere terminada |
| **Should** | Importante, pero puede quedar para el final de la semana 3 |
| **Could** | Deseable si sobra tiempo |
| **Won't** | Explícitamente fuera de la beta |

---

## 4. Plantilla de caso de uso

Cada caso de uso se guarda en un archivo propio y sigue esta estructura:

```markdown
# CU-XX — Nombre del caso de uso

| Campo | Valor |
|---|---|
| Módulo | ... |
| Actores | ... |
| Prioridad | Must / Should / Could |
| Diagrama | ... |

## Objetivo
...

## Precondiciones
...

## Disparador
...

## Flujo principal
1. ...
2. ...

## Flujos alternativos
### A1 — Nombre
- Cuándo ocurre: ...
- Respuesta del sistema: ...

## Postcondiciones
...

## Reglas de negocio
- ...

## Datos y servicios involucrados
- ...

## Seguridad
- ...

## Criterios de aceptación
- [ ] ...
```

---

## 5. Convenciones

- Un archivo por caso de uso: `cu-XX-nombre-corto.md`.
- Los flujos se numeran y describen acciones del actor o del sistema, no detalles de código.
- Cada caso referencia el diagrama que lo ilustra, si existe.
- Los errores se describen por comportamiento, no por mensaje exacto.
- El `user_id` siempre sale del token, nunca del cuerpo de la petición ni de la URL.
- Los casos con varios subflujos (CU-16, CU-20) se mantienen en un solo archivo para no duplicar reglas.
- La documentación se escribe en español; los identificadores técnicos quedan en inglés.

---

## 6. Estado

| Casos | Estado |
|---|---|
| CU-01 a CU-25 | Redactados |

---

## 7. Fuera del alcance de la beta

Estos casos **no** se documentan como parte de la beta:

- Pago con pasarela real.
- Facturación electrónica.
- Cálculo real de envíos o integración con transportadoras.
- Recuperación de contraseña por correo y verificación de correo.
- Reseñas, wishlist y fidelización.
- Flujo B2B completo.
- Aplicación móvil nativa.
- Gestión de usuarios y roles desde el panel administrativo.
- Cancelación de pedidos y cupones de descuento.

---

## 8. Relación con otros documentos

| Documento | Relación |
|---|---|
| [`../diagrams/`](../diagrams/README.md) | Cada caso enlaza al diagrama que lo representa |
| [`RESUMEN.md`](RESUMEN.md) | Explica el conjunto y las decisiones tomadas |
| `../architecture.md` | Explica cómo los servicios soportan estos casos |
| `../api/` | Los contratos OpenAPI implementan los flujos aquí descritos |
| `../security.md` | Detalla los controles aplicados en cada caso |
| `../beta-criteria.md` | Convierte los casos `Must` en criterios de aceptación |
