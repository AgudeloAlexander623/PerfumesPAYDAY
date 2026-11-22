# Resumen de los casos de uso

Se crearon 25 casos de uso en `docs/use-cases/`, uno por archivo, más un `README.md` con el índice, los actores y la plantilla. Cubren los seis módulos de la beta: autenticación y cuenta (7), catálogo (4), carrito (5), checkout y direcciones (2), pedidos (2) y administración (5). De ellos, 18 son Must, 6 Should y 1 Could.

Cada documento sigue la misma estructura: objetivo, precondiciones, disparador, flujo principal, flujos alternativos, postcondiciones, reglas de negocio, datos y servicios, seguridad y criterios de aceptación. Esa uniformidad permite compararlos, convertirlos en contratos de API y derivar pruebas.

El propósito es acordar el comportamiento antes de implementar. Describe qué logra el actor y qué responde el sistema; no impone clases ni endpoints. Por eso sirve como puente entre el README, los diagramas y el futuro código.

## Qué aporta cada bloque

- **Autenticación y cuenta:** registro, inicio y renovación de sesión, cierre, perfil y cambio de contraseña.
- **Catálogo:** exploración, búsqueda con filtros, detalle con presentaciones y página de mayoristas.
- **Carrito:** agregar, ver, actualizar, eliminar y fusionar el carrito de invitado con el del usuario.
- **Checkout:** direcciones, revalidación de precio y stock, snapshot del pedido e idempotencia.
- **Pedidos:** historial y detalle con control de propiedad.
- **Administración:** productos, pedidos, estados, auditoría, marcas y categorías.

## Decisiones principales

- Se consolidaron dos casos para evitar redundancia: "cerrar sesión en todos los dispositivos" quedó como flujo alternativo del CU-04, y "consultar auditoría" se integró al CU-23. El catálogo final tiene 25 casos, no 27.
- El carrito es híbrido: invitado en `localStorage` (solo identificadores y cantidades) y autenticado en `order-service`. Al iniciar sesión se fusiona con topes de stock y clave de idempotencia (CU-15).
- Los precios nunca se confían al cliente. Se revalidan al ver el carrito y al crear el pedido; el pedido guarda un snapshot inmutable de productos, precios y dirección (CU-17).
- La seguridad se trata como regla de negocio: el `user_id` sale del token, se responde 404 ante recursos ajenos para evitar IDOR, y el rol admin se valida en el servidor (CU-19, CU-20, CU-22).
- El checkout usa idempotencia y transacciones para no duplicar pedidos ni dejar stock descontado a medias (CU-17).
- La auditoría es append-only y cada servicio es dueño de la suya; no se hacen joins entre bases de datos (CU-23).

## Riesgos que se controlan

- Doble clic o reintento de red al comprar: idempotencia en carrito y checkout.
- Acceso a pedidos o direcciones ajenas: filtro por `user_id` y respuesta `404`.
- Precio manipulado desde el navegador: recálculo en el servidor.
- Pérdida del carrito al iniciar sesión: fusión con topes de stock.
- Cambios administrativos sin rastro: auditoría append-only.
- Tokens robados: rotación del refresh y revocación de sesiones.

También se delimitó el alcance: quedan fuera pagos reales, recuperación por correo, cancelación de pedidos, cupones, reseñas, B2B y gestión de usuarios. Nombrarlos evita que aparezcan a mitad de la beta.

## Cómo leerlos

Se recomienda empezar por el `README.md` y seguir el orden de los lotes: sesión, catálogo, carrito, checkout, pedidos y administración. Los Must son la base de la beta; los Should y Could están redactados con el mismo formato, pero pueden recortarse si el tiempo no alcanza.

## Convenciones

La documentación está en español y los identificadores en inglés. Cada archivo usa kebab-case, los errores se describen por comportamiento y cada caso enlaza a su diagrama. Los casos con varios subflujos, como direcciones y productos, se mantienen en un solo documento para no repetir reglas.

El siguiente paso es convertir los casos Must en contratos OpenAPI, ADRs y criterios de beta. Con estos documentos ya existe una fuente única para saber qué debe hacer el sistema y cómo demostrar que funciona.
