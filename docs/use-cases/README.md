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
| CU-01 | Registrarse | Visitante | Must | 03 |
| CU-02 | Iniciar sesión | Visitante | Must | 03 |
| CU-03 | Renovar sesión | Cliente | Must | 03 |
| CU-04 | Cerrar sesión | Cliente / Administrador | Must | 03 |
| CU-05 | Consultar perfil | Cliente | Should | — |
| CU-06 | Editar perfil | Cliente | Could | — |

### Catálogo

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| CU-07 | Explorar catálogo | Visitante / Cliente | Must | 04 |
| CU-08 | Buscar y filtrar productos | Visitante / Cliente | Must | 04 |
| CU-09 | Ver detalle de producto | Visitante / Cliente | Must | 04 |
| CU-10 | Ver página de mayoristas | Visitante / Cliente | Should | — |

### Carrito

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| CU-11 | Agregar producto al carrito | Cliente / Visitante | Must | 05 |
| CU-12 | Ver carrito | Cliente / Visitante | Must | 05 |
| CU-13 | Actualizar cantidad | Cliente / Visitante | Must | 05 |
| CU-14 | Eliminar producto del carrito | Cliente / Visitante | Must | 05 |
| CU-15 | Fusionar carrito al iniciar sesión | Cliente | Must | 05 |

### Checkout y direcciones

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| CU-16 | Gestionar direcciones de envío | Cliente | Must | 06 |
| CU-17 | Realizar checkout simulado | Cliente | Must | 06 |

### Pedidos

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| CU-18 | Consultar historial de pedidos | Cliente | Must | 07 |
| CU-19 | Ver detalle de un pedido | Cliente | Must | 07 |

### Administración

| ID | Caso de uso | Actor principal | Prioridad | Diagrama |
|---|---|---|---|---|
| CU-20 | Gestionar productos | Administrador | Must | 08 |
| CU-21 | Consultar pedidos | Administrador | Must | 08 |
| CU-22 | Revisar estado de un pedido | Administrador | Should | 08 |
| CU-23 | Auditar acciones administrativas | Sistema | Should | 08 |

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
- La documentación se escribe en español; los identificadores técnicos quedan en inglés.

---

## 6. Estado

| Caso | Estado |
|---|---|
| CU-01 | Redactado |
| CU-02 a CU-23 | Pendientes |

---

## 7. Fuera del alcance de la beta

Estos casos **no** se documentan como parte de la beta:

- Pago con pasarela real.
- Facturación electrónica.
- Cálculo real de envíos o integración con transportadoras.
- Reseñas, wishlist y fidelización.
- Flujo B2B completo.
- Aplicación móvil nativa.
- Gestión de usuarios y roles desde el panel administrativo.

---

## 8. Relación con otros documentos

| Documento | Relación |
|---|---|
| [`../diagrams/`](../diagrams/README.md) | Cada caso enlaza al diagrama que lo representa |
| `../architecture.md` | Explica cómo los servicios soportan estos casos |
| `../api/` | Los contratos OpenAPI implementan los flujos aquí descritos |
| `../security.md` | Detalla los controles aplicados en cada caso |
| `../beta-criteria.md` | Convierte los casos `Must` en criterios de aceptación |
