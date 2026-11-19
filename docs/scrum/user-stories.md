# Historias de usuario — PerfumesPAYDAY

> **Estado:** borrador 0.2 — alineado con los 25 casos de uso (CU-01 a CU-25) y con el ADR-0007 (carrito híbrido).
> **Última actualización:** 2026-11-11
> **Fuente de verdad:** el comportamiento funcional vive en [`../use-cases/`](../use-cases/README.md). Este documento **deriva** de esos casos de uso y no los reemplaza: ante cualquier conflicto, gana el caso de uso.
> **Siguiente paso:** convertir cada historia en una tarjeta del tablero y, junto con el equipo, en contratos OpenAPI por servicio.

---

## 1. Propósito del documento

Este documento traduce los casos de uso del proyecto a **historias de usuario** para alimentar el backlog del tablero (GitHub Projects) y dar un lenguaje común al equipo, al profesor y a los asistentes de IA.

Cada historia declara **quién** la usa, **qué** necesita y **para qué**, y **cómo** se comprobará que quedó bien. Una historia está lista para programar cuando cumple el *Definition of Ready* (sección 11).

### 1.1 Formato de una historia

| Parte | Pregunta que responde | Ejemplo |
|---|---|---|
| Historia | ¿Quién quiere qué y para qué? | *Como cliente, quiero iniciar sesión, para ver mis pedidos.* |
| Criterios de aceptación | ¿Cómo se comprueba? | *Dado que…, cuando…, entonces…* |
| Reglas y notas | ¿Qué no se puede olvidar? | *Solo veo mis propios pedidos.* |

Los criterios usan el formato **Dado / Cuando / Entonces** (Gherkin): *Dado* es la situación de partida, *Cuando* la acción de la persona y *Entonces* el resultado esperado. Si cada criterio se puede demostrar, la historia está terminada.

---

## 2. Actores

| Actor | Descripción | Rol técnico |
|---|---|---|
| **Visitante** | Persona sin sesión iniciada; explora el catálogo. | — |
| **Cliente** | Persona registrada; compra y consulta sus pedidos. | `cliente` |
| **Administrador** | Persona que gestiona catálogo y pedidos desde el panel. | `admin` |
| **Sistema** | Servicios internos que validan y ejecutan tareas. | — |
| **Equipo de desarrollo** | Responsable de las historias técnicas (sección 6). | — |

> Los únicos roles válidos son **`cliente`** y **`admin`** (seed [`Databases/seeds/001_roles.sql`](../../Databases/seeds/001_roles.sql)). El rol nunca lo elige el usuario: el registro público siempre crea `cliente` y el rol `admin` se asigna por fuera de la aplicación.

---

## 3. Organización del backlog

Las historias se agrupan en **épicas**. Cada épica coincide con una *swimlane* del tablero para facilitar la asignación.

| Épica | Nombre | Servicio principal |
|---|---|---|
| EP-01 | Cuentas y sesión | `security-service` |
| EP-02 | Catálogo | `catalog-service` |
| EP-03 | Carrito | `order-service` + frontend |
| EP-04 | Checkout y pedidos | `order-service` |
| EP-05 | Administración | `catalog-service` / `order-service` |
| EP-06 | Calidad transversal | todos (sección 10) |

**Prioridad (MoSCoW):**

- **Must** — obligatorio; sin esto la beta no cumple los criterios de aceptación del README.
- **Should** — importante; puede entregarse al final de la semana 3.
- **Could** — deseable si sobra tiempo.

**Semana** indica el sprint propuesto según el cronograma del README. Es una propuesta que el equipo ajusta en la planeación.

> Regla de recorte: primero se recorta B2B, administración avanzada y filtros. **Nunca** seguridad ni checkout.

---

## 4. Índice de historias

| ID | Historia | Actor | Épica | Prioridad | Semana | Caso de uso |
|---|---|---|---|---|---|---|
| HU-01 | Registrarme | Visitante | EP-01 | Must | 1 | [CU-01](../use-cases/cu-01-registro.md) |
| HU-02 | Iniciar sesión | Visitante | EP-01 | Must | 1 | [CU-02](../use-cases/cu-02-inicio-sesion.md) |
| HU-03 | Renovar mi sesión | Cliente / Admin | EP-01 | Must | 1 | [CU-03](../use-cases/cu-03-renovar-sesion.md) |
| HU-04 | Cerrar sesión | Cliente / Admin | EP-01 | Must | 1 | [CU-04](../use-cases/cu-04-cerrar-sesion.md) |
| HU-05 | Consultar mi perfil | Cliente | EP-01 | Should | 3 | [CU-05](../use-cases/cu-05-consultar-perfil.md) |
| HU-06 | Editar mi perfil | Cliente | EP-01 | Could | 3 | [CU-06](../use-cases/cu-06-editar-perfil.md) |
| HU-07 | Cambiar mi contraseña | Cliente / Admin | EP-01 | Should | 3 | [CU-24](../use-cases/cu-24-cambiar-contrasena.md) |
| HU-08 | Explorar el catálogo | Visitante / Cliente | EP-02 | Must | 1 | [CU-07](../use-cases/cu-07-explorar-catalogo.md) |
| HU-09 | Buscar y filtrar productos | Visitante / Cliente | EP-02 | Must | 2 | [CU-08](../use-cases/cu-08-buscar-filtrar-productos.md) |
| HU-10 | Ver el detalle de un producto | Visitante / Cliente | EP-02 | Must | 1 | [CU-09](../use-cases/cu-09-ver-detalle-producto.md) |
| HU-11 | Ver la página de mayoristas | Visitante / Cliente | EP-02 | Should | 3 | [CU-10](../use-cases/cu-10-pagina-mayoristas.md) |
| HU-12 | Agregar productos al carrito | Visitante / Cliente | EP-03 | Must | 2 | [CU-11](../use-cases/cu-11-agregar-al-carrito.md) |
| HU-13 | Ver mi carrito | Visitante / Cliente | EP-03 | Must | 2 | [CU-12](../use-cases/cu-12-ver-carrito.md) |
| HU-14 | Actualizar cantidades del carrito | Visitante / Cliente | EP-03 | Must | 2 | [CU-13](../use-cases/cu-13-actualizar-cantidad.md) |
| HU-15 | Eliminar productos del carrito | Visitante / Cliente | EP-03 | Must | 2 | [CU-14](../use-cases/cu-14-eliminar-del-carrito.md) |
| HU-16 | Fusionar mi carrito al iniciar sesión | Cliente | EP-03 | Must | 2 | [CU-15](../use-cases/cu-15-fusionar-carrito.md) |
| HU-17 | Gestionar mis direcciones de envío | Cliente | EP-04 | Must | 2 | [CU-16](../use-cases/cu-16-gestionar-direcciones.md) |
| HU-18 | Confirmar mi compra (checkout simulado) | Cliente | EP-04 | Must | 2 | [CU-17](../use-cases/cu-17-checkout-simulado.md) |
| HU-19 | Consultar mi historial de pedidos | Cliente | EP-04 | Must | 2 | [CU-18](../use-cases/cu-18-historial-pedidos.md) |
| HU-20 | Ver el detalle de un pedido | Cliente | EP-04 | Must | 2 | [CU-19](../use-cases/cu-19-detalle-pedido.md) |
| HU-21 | Gestionar productos | Administrador | EP-05 | Must | 2 | [CU-20](../use-cases/cu-20-gestionar-productos.md) |
| HU-22 | Consultar los pedidos de la tienda | Administrador | EP-05 | Must | 2 | [CU-21](../use-cases/cu-21-consultar-pedidos-admin.md) |
| HU-23 | Revisar y avanzar el estado de un pedido | Administrador | EP-05 | Should | 3 | [CU-22](../use-cases/cu-22-revisar-estado-pedido.md) |
| HU-24 | Auditar las acciones administrativas | Administrador | EP-05 | Should | 3 | [CU-23](../use-cases/cu-23-auditar-acciones.md) |
| HU-25 | Gestionar marcas y categorías | Administrador | EP-05 | Should | 3 | [CU-25](../use-cases/cu-25-gestionar-marcas-categorias.md) |

**Total: 25 historias** — una por cada caso de uso, con trazabilidad directa. Las 15 historias técnicas (HT-01 a HT-15) están en [`../scrum/technical-stories.md`](../scrum/technical-stories.md).

---

## 5. Historias de usuario

### EP-01 · Cuentas y sesión

#### HU-01 · Registrarme
*Caso de uso: [CU-01](../use-cases/cu-01-registro.md) · Prioridad: Must · Semana 1*

**Como** visitante, **quiero** crear una cuenta con mi correo y una contraseña, **para** poder comprar y consultar mis pedidos.

**Criterios de aceptación**

- **Dado** que no tengo cuenta, **cuando** completo el formulario con datos válidos, **entonces** mi cuenta se crea con el rol `cliente` y puedo iniciar sesión.
- **Dado** que el correo ya está registrado, **cuando** intento registrarme con él, **entonces** veo un mensaje claro y no se crea una cuenta duplicada.
- **Dado** que la contraseña no cumple las reglas, **cuando** envío el formulario, **entonces** veo qué debo corregir.
- **Dado** que supero el límite de intentos permitido, **cuando** sigo enviando solicitudes, **entonces** el sistema me bloquea temporalmente (`429`).

**Reglas y notas**

- El registro público siempre crea el rol `cliente`; nadie se registra como `admin`.
- La contraseña se guarda con Argon2 o bcrypt, nunca en texto plano.
- Los mensajes de error no revelan si un correo existe.

---

#### HU-02 · Iniciar sesión
*Caso de uso: [CU-02](../use-cases/cu-02-inicio-sesion.md) · Prioridad: Must · Semana 1*

**Como** visitante con cuenta, **quiero** iniciar sesión con mi correo y contraseña, **para** acceder a mis funciones de cliente.

**Criterios de aceptación**

- **Dado** que tengo cuenta, **cuando** ingreso credenciales correctas, **entonces** inicio sesión y recibo un token de acceso y un refresh token.
- **Dado** que me equivoco en el correo o la contraseña, **cuando** intento entrar, **entonces** veo un mensaje genérico de "credenciales inválidas" que no indica cuál dato falló.
- **Dado** que supero el límite de intentos fallidos, **cuando** insisto, **entonces** el sistema me bloquea temporalmente (`429`).

**Reglas y notas**

- Solo `security-service` emite tokens.
- El mensaje genérico evita que un atacante descubra qué correos existen.

---

#### HU-03 · Renovar mi sesión
*Caso de uso: [CU-03](../use-cases/cu-03-renovar-sesion.md) · Prioridad: Must · Semana 1*

**Como** cliente o administrador, **quiero** que mi sesión se renueve sola mientras uso el sitio, **para** no tener que iniciar sesión cada pocos minutos.

**Criterios de aceptación**

- **Dado** que mi token de acceso venció pero mi refresh token sigue vigente, **cuando** hago una acción, **entonces** la sesión se renueva sin interrumpirme.
- **Dado** que mi refresh token también venció o fue revocado, **cuando** hago una acción, **entonces** se me pide iniciar sesión de nuevo.
- **Dado** que un refresh token ya usado se vuelve a presentar, **cuando** llega al servidor, **entonces** se rechaza (rotación de tokens).

**Reglas y notas**

- El refresh token se guarda como hash y se rota en cada uso.

---

#### HU-04 · Cerrar sesión
*Caso de uso: [CU-04](../use-cases/cu-04-cerrar-sesion.md) · Prioridad: Must · Semana 1*

**Como** cliente o administrador, **quiero** cerrar mi sesión, **para** proteger mi cuenta cuando termino de usar el sitio.

**Criterios de aceptación**

- **Dado** que tengo sesión iniciada, **cuando** cierro sesión, **entonces** vuelvo al estado de visitante y mi refresh token se revoca.
- **Dado** que cerré sesión, **cuando** intento entrar a una página protegida, **entonces** se me pide iniciar sesión de nuevo.
- **Dado** que elijo cerrar sesión en todos los dispositivos, **cuando** lo confirmo, **entonces** se revocan todas mis sesiones activas.

---

#### HU-05 · Consultar mi perfil
*Caso de uso: [CU-05](../use-cases/cu-05-consultar-perfil.md) · Prioridad: Should · Semana 3*

**Como** cliente, **quiero** ver los datos de mi cuenta, **para** confirmar que mi información es correcta.

**Criterios de aceptación**

- **Dado** que tengo sesión, **cuando** abro "Mi perfil", **entonces** veo mi nombre, correo, rol, fecha de registro y último acceso.
- **Dado** que consulto mi perfil, **cuando** llega la respuesta, **entonces** no incluye `password_hash` ni identificadores internos de sesión.
- **Dado** que intento consultar el perfil de otra persona, **cuando** lo solicito, **entonces** el servidor lo rechaza.

**Reglas y notas**

- El `user_id` sale del token, nunca de la URL.
- El correo es de solo lectura en la beta.

---

#### HU-06 · Editar mi perfil
*Caso de uso: [CU-06](../use-cases/cu-06-editar-perfil.md) · Prioridad: Could · Semana 3*

**Como** cliente, **quiero** actualizar mi nombre, **para** mantener mis datos al día.

**Criterios de aceptación**

- **Dado** que tengo sesión, **cuando** cambio mi nombre y guardo, **entonces** el perfil muestra el nuevo nombre.
- **Dado** que envío un nombre vacío o demasiado largo, **cuando** guardo, **entonces** veo qué corregir (`400`/`422`).
- **Dado** que intento cambiar mi correo o mi rol, **cuando** guardo, **entonces** el servidor ignora esos campos.

**Reglas y notas**

- Solo el nombre es editable (lista blanca de campos); el correo y el rol son inmutables.

---

#### HU-07 · Cambiar mi contraseña
*Caso de uso: [CU-24](../use-cases/cu-24-cambiar-contrasena.md) · Prioridad: Should · Semana 3*

**Como** cliente o administrador, **quiero** cambiar mi contraseña conociendo la actual, **para** proteger mi cuenta sin depender del correo.

**Criterios de aceptación**

- **Dado** que ingreso mi contraseña actual correcta y una nueva válida, **cuando** confirmo, **entonces** la contraseña se actualiza y todas mis sesiones se revocan.
- **Dado** que la contraseña actual es incorrecta, **cuando** confirmo, **entonces** recibo `401` con un mensaje genérico.
- **Dado** que la nueva contraseña es débil o igual a la actual, **cuando** confirmo, **entonces** recibo `422` o `400` con la explicación.

**Reglas y notas**

- Siempre se exige la contraseña actual.
- No se envía la contraseña por correo; la recuperación está fuera de alcance.

---

### EP-02 · Catálogo

#### HU-08 · Explorar el catálogo
*Caso de uso: [CU-07](../use-cases/cu-07-explorar-catalogo.md) · Prioridad: Must · Semana 1*

**Como** visitante o cliente, **quiero** ver el catálogo de perfumes, **para** explorar lo que la tienda ofrece.

**Criterios de aceptación**

- **Dado** que entro al catálogo, **cuando** carga, **entonces** veo los productos con su nombre, marca y precio de referencia en COP.
- **Dado** que entro como visitante, **cuando** navego, **entonces** veo el catálogo completo sin necesidad de cuenta.
- **Dado** que no hay productos que mostrar, **cuando** carga el listado, **entonces** veo un mensaje que lo explica en lugar de una pantalla vacía.

**Reglas y notas**

- La beta tendrá entre 25 y 30 productos simulados.
- Los precios se muestran en COP con IVA incluido (supuesto del simulador).

---

#### HU-09 · Buscar y filtrar productos
*Caso de uso: [CU-08](../use-cases/cu-08-buscar-filtrar-productos.md) · Prioridad: Must · Semana 2*

**Como** visitante o cliente, **quiero** buscar y filtrar por marca, género y familia olfativa, **para** encontrar rápido lo que me interesa.

**Criterios de aceptación**

- **Dado** que escribo un texto, **cuando** busco, **entonces** veo los productos cuyo nombre o marca coincide.
- **Dado** que aplico varios filtros, **cuando** los combino, **entonces** veo solo los productos que cumplen todos a la vez.
- **Dado** que ningún producto cumple los filtros, **cuando** los aplico, **entonces** veo un mensaje que me sugiere quitarlos.
- **Dado** que apliqué filtros, **cuando** los limpio, **entonces** vuelvo a ver el catálogo completo.
- **Dado** que escribo caracteres especiales o código, **cuando** busco, **entonces** el sistema lo trata como texto simple y no se ejecuta nada.

**Reglas y notas**

- La búsqueda usa consultas parametrizadas (protege contra inyección SQL) y escapado de salida (protege contra XSS).

---

#### HU-10 · Ver el detalle de un producto
*Caso de uso: [CU-09](../use-cases/cu-09-ver-detalle-producto.md) · Prioridad: Must · Semana 1*

**Como** visitante o cliente, **quiero** ver la información completa de un perfume, **para** decidir qué presentación comprar.

**Criterios de aceptación**

- **Dado** que abro un producto, **cuando** carga el detalle, **entonces** veo marca, género, familia olfativa, presentaciones disponibles, precio y stock.
- **Dado** que elijo otra presentación, **cuando** la selecciono, **entonces** el precio y el stock se actualizan a los de esa presentación.
- **Dado** que una presentación está agotada, **cuando** la miro, **entonces** veo que está agotada y no puedo agregarla al carrito.
- **Dado** que el producto no existe, **cuando** abro su dirección, **entonces** veo un mensaje de "producto no encontrado".

**Reglas y notas**

- Las presentaciones son de 30, 50 y 100 ml.
- El stock es simulado.

---

#### HU-11 · Ver la página de mayoristas
*Caso de uso: [CU-10](../use-cases/cu-10-pagina-mayoristas.md) · Prioridad: Should · Semana 3*

**Como** visitante o cliente, **quiero** encontrar la sección de mayoristas, **para** saber que la tienda planea ofrecerla.

**Criterios de aceptación**

- **Dado** que entro a la página de mayoristas, **cuando** carga, **entonces** veo un mensaje de "Próximamente".
- **Dado** que estoy en esa página, **cuando** la reviso, **entonces** no hay formulario funcional ni precios al por mayor.

**Reglas y notas**

- Es una página estática del frontend; no genera endpoints ni lógica B2B en la beta.

---

### EP-03 · Carrito

#### HU-12 · Agregar productos al carrito
*Caso de uso: [CU-11](../use-cases/cu-11-agregar-al-carrito.md) · Prioridad: Must · Semana 2*

**Como** visitante o cliente, **quiero** agregar la presentación que me gusta, **para** juntar mis compras antes de pagar.

**Criterios de aceptación**

- **Dado** que estoy en el detalle de un producto con stock, **cuando** agrego una presentación, **entonces** aparece en mi carrito con su cantidad y el contador se actualiza.
- **Dado** que ya tengo esa presentación en el carrito, **cuando** la agrego otra vez, **entonces** se suma a la cantidad existente sin duplicar la línea.
- **Dado** que pido más unidades que el stock disponible, **cuando** intento agregarlas, **entonces** veo un aviso y no se supera el stock.
- **Dado** que no tengo sesión, **cuando** agrego productos, **entonces** se conservan en mi navegador durante la sesión.

**Reglas y notas**

- Carrito **híbrido** ([ADR-0007](../adr/0007-carrito-hibrido.md)): el visitante lo guarda en `localStorage` (solo `variant_id` y cantidad) y el cliente autenticado en `order-service`.
- El precio nunca se guarda como fuente de verdad; se consulta al servidor.

---

#### HU-13 · Ver mi carrito
*Caso de uso: [CU-12](../use-cases/cu-12-ver-carrito.md) · Prioridad: Must · Semana 2*

**Como** visitante o cliente, **quiero** ver el contenido y el total de mi carrito, **para** revisar mi compra antes de pagar.

**Criterios de aceptación**

- **Dado** que tengo productos, **cuando** abro el carrito, **entonces** veo cada ítem con su presentación, cantidad, precio vigente y subtotal.
- **Dado** que abro mi carrito autenticado, **cuando** carga, **entonces** los precios y el total se recalculan contra el servidor.
- **Dado** que el carrito está vacío, **cuando** lo abro, **entonces** veo un mensaje que me invita a explorar el catálogo.

---

#### HU-14 · Actualizar cantidades del carrito
*Caso de uso: [CU-13](../use-cases/cu-13-actualizar-cantidad.md) · Prioridad: Must · Semana 2*

**Como** visitante o cliente, **quiero** cambiar las cantidades de mi carrito, **para** ajustar mi compra antes de confirmarla.

**Criterios de aceptación**

- **Dado** que cambio una cantidad, **cuando** confirmo, **entonces** el subtotal y el total se recalculan.
- **Dado** que pongo una cantidad mayor al stock, **cuando** confirmo, **entonces** se ajusta al máximo disponible con un aviso.
- **Dado** que pongo una cantidad inválida (cero, negativa o decimal), **cuando** confirmo, **entonces** el sistema la rechaza.

---

#### HU-15 · Eliminar productos del carrito
*Caso de uso: [CU-14](../use-cases/cu-14-eliminar-del-carrito.md) · Prioridad: Must · Semana 2*

**Como** visitante o cliente, **quiero** quitar productos del carrito, **para** descartar lo que no voy a comprar.

**Criterios de aceptación**

- **Dado** que quito un producto, **cuando** confirmo, **entonces** desaparece del carrito y el total se actualiza.
- **Dado** que dejo la cantidad en cero, **cuando** confirmo el cambio, **entonces** el producto se elimina.
- **Dado** que vacío el carrito, **cuando** lo miro, **entonces** veo un mensaje que me invita a explorar el catálogo.

---

#### HU-16 · Fusionar mi carrito al iniciar sesión
*Caso de uso: [CU-15](../use-cases/cu-15-fusionar-carrito.md) · Prioridad: Must · Semana 2*

**Como** cliente, **quiero** que el carrito que armé como visitante se una al de mi cuenta al iniciar sesión, **para** no perder mi selección.

**Criterios de aceptación**

- **Dado** que armé un carrito como visitante, **cuando** inicio sesión, **entonces** ese carrito se fusiona con el de mi cuenta y el carrito de invitado se borra.
- **Dado** que un producto está repetido en ambos carritos, **cuando** se fusionan, **entonces** las cantidades se suman sin duplicar líneas.
- **Dado** que la suma supera el stock, **cuando** se fusiona, **entonces** la cantidad se ajusta al máximo disponible.
- **Dado** que algunos ítems ya no están disponibles, **cuando** se fusiona, **entonces** se omiten y se me informa.
- **Dado** que la fusión falla por un problema de red, **cuando** reintento, **entonces** no se duplican cantidades y mi carrito de invitado se conserva.

**Reglas y notas**

- La fusión es idempotente y nunca mezcla el carrito de otra persona.

---

### EP-04 · Checkout y pedidos

#### HU-17 · Gestionar mis direcciones de envío
*Caso de uso: [CU-16](../use-cases/cu-16-gestionar-direcciones.md) · Prioridad: Must · Semana 2*

**Como** cliente, **quiero** crear y administrar mis direcciones de envío, **para** elegir dónde recibir mi pedido.

**Criterios de aceptación**

- **Dado** que tengo sesión, **cuando** creo mi primera dirección, **entonces** queda guardada y marcada como predeterminada.
- **Dado** que tengo direcciones, **cuando** abro la lista, **entonces** veo solo las mías y cuál es la predeterminada.
- **Dado** que edito una dirección o marco otra como predeterminada, **cuando** guardo, **entonces** el cambio se refleja y solo queda una predeterminada.
- **Dado** que elimino una dirección, **cuando** confirmo, **entonces** desaparece y los pedidos anteriores conservan su copia.
- **Dado** que intento ver o editar una dirección de otra persona, **cuando** lo hago, **entonces** recibo `404`.
- **Dado** que dejo campos obligatorios vacíos o inválidos, **cuando** guardo, **entonces** veo qué corregir (`400`/`422`).

**Reglas y notas**

- El departamento y la ciudad se validan contra la lista de Colombia; el teléfono se guarda como texto.
- Solo puede existir una dirección predeterminada por usuario.

---

#### HU-18 · Confirmar mi compra (checkout simulado)
*Caso de uso: [CU-17](../use-cases/cu-17-checkout-simulado.md) · Prioridad: Must · Semana 2*

**Como** cliente, **quiero** confirmar mi carrito eligiendo una dirección, **para** generar un pedido simulado.

**Criterios de aceptación**

- **Dado** que tengo sesión, ítems en el carrito y una dirección, **cuando** confirmo la compra, **entonces** se crea un pedido con una copia de productos, precios y dirección.
- **Dado** que no he iniciado sesión, **cuando** intento confirmar, **entonces** se me pide iniciar sesión y luego puedo continuar.
- **Dado** que un precio cambió o el stock ya no alcanza, **cuando** confirmo, **entonces** el sistema me avisa y no crea el pedido con datos desactualizados (`409`).
- **Dado** que confirmo la compra, **cuando** termina, **entonces** el pago queda marcado como simulado y mi carrito se vacía.
- **Dado** que hago doble clic o se repite el envío, **cuando** llega la misma clave de idempotencia, **entonces** se crea un solo pedido y se devuelve el original.
- **Dado** que falla el descuento de stock, **cuando** ocurre, **entonces** el pedido se revierte y no quedan estados parciales.
- **Dado** que la compra terminó, **cuando** veo la confirmación, **entonces** aparecen el número de pedido, los productos, el total y que el pago es simulado.

**Reglas y notas**

- El servidor recalcula subtotales y total; nunca confía en montos del navegador.
- El pedido guarda un **snapshot** inmutable (nombre, presentación y precio del momento).
- La clave de idempotencia es obligatoria para evitar pedidos duplicados.
- No se llama a ninguna pasarela real ni se piden datos de tarjeta.

---

#### HU-19 · Consultar mi historial de pedidos
*Caso de uso: [CU-18](../use-cases/cu-18-historial-pedidos.md) · Prioridad: Must · Semana 2*

**Como** cliente, **quiero** ver la lista de mis pedidos anteriores, **para** hacer seguimiento de lo que he comprado.

**Criterios de aceptación**

- **Dado** que tengo sesión, **cuando** abro mi historial, **entonces** veo solo mis pedidos, del más reciente al más antiguo, con su estado actual.
- **Dado** que no he hecho pedidos, **cuando** abro mi historial, **entonces** veo un mensaje que lo indica.
- **Dado** que otro cliente tiene pedidos, **cuando** abro mi historial, **entonces** nunca aparecen los suyos.

---

#### HU-20 · Ver el detalle de un pedido
*Caso de uso: [CU-19](../use-cases/cu-19-detalle-pedido.md) · Prioridad: Must · Semana 2*

**Como** cliente, **quiero** abrir uno de mis pedidos, **para** revisar qué compré y cuánto pagué.

**Criterios de aceptación**

- **Dado** que abro un pedido mío, **cuando** carga, **entonces** veo los productos tal como estaban al comprar (nombre, presentación y precio del snapshot), la dirección de envío y el total.
- **Dado** que cambio el identificador en la dirección por el de un pedido ajeno, **cuando** intento abrirlo, **entonces** el servidor responde `404`.

**Reglas y notas**

- Es la prueba clásica de IDOR que hará el profesor; debe quedar cubierta por una prueba automática.

---

### EP-05 · Administración

#### HU-21 · Gestionar productos
*Caso de uso: [CU-20](../use-cases/cu-20-gestionar-productos.md) · Prioridad: Must · Semana 2*

**Como** administrador, **quiero** crear, editar y desactivar productos y sus presentaciones, **para** mantener el catálogo al día.

**Criterios de aceptación**

- **Dado** que soy `admin`, **cuando** creo un producto con datos válidos y sus presentaciones, **entonces** aparece en el catálogo.
- **Dado** que dejo campos obligatorios vacíos o con valores inválidos (por ejemplo, un precio negativo), **cuando** guardo, **entonces** veo qué corregir y no se guarda nada.
- **Dado** que edito un producto, **cuando** guardo, **entonces** el catálogo muestra los cambios y los pedidos anteriores conservan su snapshot.
- **Dado** que desactivo un producto, **cuando** confirmo, **entonces** deja de ofrecerse, pero los pedidos anteriores siguen mostrándose correctamente.
- **Dado** que soy `cliente`, **cuando** intento gestionar productos, **entonces** el servidor responde `403`.

**Reglas y notas**

- Los datos se validan en el servidor, no solo en el formulario.
- Cada cambio queda auditado (HU-24).

---

#### HU-22 · Consultar los pedidos de la tienda
*Caso de uso: [CU-21](../use-cases/cu-21-consultar-pedidos-admin.md) · Prioridad: Must · Semana 2*

**Como** administrador, **quiero** ver todos los pedidos realizados, **para** conocer la actividad de la tienda.

**Criterios de aceptación**

- **Dado** que soy `admin`, **cuando** abro la sección de pedidos, **entonces** veo los pedidos de todos los clientes.
- **Dado** que soy `cliente`, **cuando** intento acceder a esa sección, **entonces** el servidor responde `403`.
- **Dado** que abro un pedido, **cuando** carga, **entonces** veo su detalle completo.

---

#### HU-23 · Revisar y avanzar el estado de un pedido
*Caso de uso: [CU-22](../use-cases/cu-22-revisar-estado-pedido.md) · Prioridad: Should · Semana 3*

**Como** administrador, **quiero** consultar un pedido y avanzar su estado, **para** reflejar el progreso de la entrega.

**Criterios de aceptación**

- **Dado** que soy `admin`, **cuando** abro un pedido, **entonces** veo su detalle y el historial de estados.
- **Dado** que elijo el siguiente estado permitido, **cuando** confirmo, **entonces** el pedido se actualiza y el cambio queda en el historial y en la auditoría.
- **Dado** que intento retroceder o saltar un estado, **cuando** confirmo, **entonces** recibo `409` con las transiciones válidas.
- **Dado** que otro administrador cambió el pedido primero, **cuando** confirmo, **entonces** recibo `409` y debo recargar antes de reintentar.
- **Dado** que soy `cliente`, **cuando** intento cambiar el estado, **entonces** recibo `403`.

**Reglas y notas**

- Las transiciones permitidas son: `paid` → `preparing` → `shipped` → `delivered`. No se retrocede ni se salta estados.
- La cancelación de pedidos está fuera del alcance de la beta.

---

#### HU-24 · Auditar las acciones administrativas
*Caso de uso: [CU-23](../use-cases/cu-23-auditar-acciones.md) · Prioridad: Should · Semana 3*

**Como** administrador, **quiero** que quede registro de las acciones administrativas, **para** saber quién cambió qué y cuándo.

**Criterios de aceptación**

- **Dado** que un admin crea, edita o desactiva un producto, o cambia el estado de un pedido, **cuando** la acción termina, **entonces** se guarda un registro con el actor, la acción, la entidad y la fecha (ISO 8601, UTC).
- **Dado** que consulto los registros, **cuando** los veo, **entonces** no contienen contraseñas ni datos personales sensibles.
- **Dado** que intento modificar o borrar un registro de auditoría, **cuando** lo hago, **entonces** el sistema lo impide (registro *append-only*).

**Reglas y notas**

- Cada servicio es dueño de su propia auditoría; no se hacen *joins* entre bases de datos.

---

#### HU-25 · Gestionar marcas y categorías
*Caso de uso: [CU-25](../use-cases/cu-25-gestionar-marcas-categorias.md) · Prioridad: Should · Semana 3*

**Como** administrador, **quiero** mantener las marcas y categorías, **para** que los productos y los filtros estén ordenados.

**Criterios de aceptación**

- **Dado** que soy `admin`, **cuando** creo o edito una marca o categoría, **entonces** el nombre y el slug quedan únicos.
- **Dado** que intento eliminar una marca o categoría con productos asociados, **cuando** confirmo, **entonces** el sistema no lo permite y ofrece desactivarla.
- **Dado** que creo un nombre vacío o un slug con caracteres no permitidos, **cuando** guardo, **entonces** recibo `400`/`422`.
- **Dado** que soy `cliente`, **cuando** intento gestionar marcas o categorías, **entonces** recibo `403`.

**Reglas y notas**

- Las categorías son planas en la beta; no hay subcategorías.
- El género y la familia olfativa son valores fijos del producto, no categorías.

---

## 6. Historias técnicas (habilitadoras)

Las historias técnicas **no** la "ve" un usuario, pero sin ellas las funcionales no se pueden construir, integrar, desplegar ni aprobar. Se documentan en su propio archivo:

➡️ **[`../scrum/technical-stories.md`](../scrum/technical-stories.md)** — 15 historias (HT-01 a HT-15) de infraestructura, integración, datos, seguridad y calidad.

---

## 7. Reglas de negocio transversales

Resumen de reglas que aparecen en varias historias. Si hay dudas al programar, se empieza por aquí.

1. **El servidor decide, el navegador sugiere.** Precios, stock, roles y propiedad de los pedidos se validan siempre en el backend.
2. **Un cliente solo ve lo suyo.** Todo acceso a recursos de otra persona se rechaza con `404` (IDOR).
3. **El pedido es una fotografía.** Guarda nombre, presentación y precio del momento de la compra.
4. **El pago es simulado.** Nunca se llama a una pasarela real.
5. **Moneda y fechas.** Precios en COP con IVA incluido; fechas en ISO 8601 UTC.
6. **Identificadores.** Todos los IDs son UUID.
7. **Mensajes de error seguros.** Claros para la persona, sin revelar detalles internos.
8. **Cada servicio es dueño de sus datos.** No se comparten tablas ni se hacen *joins* entre bases.
9. **Idempotencia.** La fusión del carrito y el checkout son idempotentes para evitar duplicados.

---

## 8. Fuera de alcance

Para no generar falsas expectativas, estas funcionalidades **no** tienen historia en la beta (ver sección 11 del README): pasarelas de pago reales, facturación electrónica DIAN, envíos reales o cálculo de costos con transportadoras, aplicación móvil nativa, flujo B2B completo, inventario multibodega, reseñas, wishlist, fidelización, analítica avanzada, recuperación de contraseña por correo, verificación de correo, cancelación de pedidos, cupones de descuento y gestión de usuarios y roles desde el panel.

---

## 9. Preguntas abiertas

Dudas que los casos de uso aún no resuelven. Se dejaron como **supuestos** para no frenar el trabajo, pero conviene confirmarlas y moverlas a un ADR cuando se decidan.

| # | Pregunta | Supuesto actual | Historias afectadas |
|---|---|---|---|
| 1 | ¿Qué reglas exactas tiene la contraseña (longitud, mayúsculas, símbolos)? | Se definen al diseñar `security-service`. | HU-01, HU-07 |
| 2 | ¿Cuánto dura el token de acceso y el refresh token? | Acceso de corta duración; el refresh se define al diseñar la seguridad. | HU-02, HU-03 |
| 3 | ¿Cuál es la cantidad máxima por ítem y el máximo de direcciones por usuario? | Se define con el equipo; el stock es el tope mínimo. | HU-12, HU-14, HU-17 |
| 4 | ¿El envío tiene costo? | Por definir; si lo tiene, se suma en el servidor. | HU-18 |
| 5 | ¿Cuáles son los umbrales exactos de *rate limit*? | Se definen al implementar seguridad. | HU-01, HU-02, HU-07 |

---

## 10. Definition of Done (calidad transversal)

Aplica a **todas** las historias. La funcionalidad responsive y los estados de carga/error son criterios de terminado, no historias aparte.

- [ ] Los criterios de aceptación de la historia se demuestran.
- [ ] Existe una prueba automática cuando el criterio lo permite (sobre todo seguridad e idempotencia).
- [ ] La interfaz es usable en celular, tablet y computador, sin desplazamiento horizontal.
- [ ] Hay estados de carga y de error claros; los errores no exponen detalles internos (trazas, rutas, datos técnicos).
- [ ] Los permisos se validan en el servidor, no solo en la interfaz.
- [ ] La documentación del componente y el caso de uso asociado quedan actualizados en el mismo pull request.
- [ ] El *pipeline* de integración continua pasa.

---

## 11. Definition of Ready

Una historia puede entrar a un sprint cuando:

- Tiene objetivo claro y un único resultado esperado.
- Tiene criterios de aceptación verificables.
- Sus dependencias están identificadas y resueltas o planificadas.
- Está estimada por el equipo.
- No depende de una pregunta abierta sin resolver que bloquee su implementación.

---

## 12. Mantenimiento del documento

- Cada cambio de alcance se refleja aquí **en el mismo pull request** que lo motiva.
- Si un caso de uso cambia, se actualiza la historia correspondiente y su tarjeta del tablero, y viceversa.
- Cuando se resuelve una pregunta abierta, la decisión se mueve a un ADR y se ajustan las historias afectadas.
- Toda historia nueva debe cumplir el *Definition of Ready* y trazarse a un caso de uso.

---

**Versión:** 0.2 — alineada con los 25 casos de uso
**Responsable:** Product Owner
