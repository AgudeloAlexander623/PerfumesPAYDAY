# Databases

1. Propósito y alcance
Este documento reúne, en orden cronológico, todo lo realizado en la capa de datos del
proyecto: las directrices recibidas, las decisiones tomadas, los problemas que aparecieron
y cómo se resolvieron, los archivos creados y los comandos usados para verificar cada
paso. Solo cubre la base de datos. La landing page, los esquemas de pantallas y la
instalación de Node se mencionan al final únicamente como contexto.

2. Reglas del README que condicionaron el diseño
Una base de datos por servicio: security_db , catalog_db y orders_db , sin tablas
compartidas.
PostgreSQL es el motor confirmado.
Identificadores UUID y fechas en UTC ( TIMESTAMPTZ ).
Snapshots en pedidos: el pedido guarda una copia del nombre, la presentación, el
precio y la dirección usados al comprar.
Presentaciones de 30, 50 y 100 ml, precios de referencia en COP y un catálogo de unos
25 a 30 productos simulados.
Pago simulado: sin pasarelas reales ni facturación electrónica de la DIAN.
Seguridad: roles verificados en el servidor, contraseñas con hash, auditoría de las
acciones administrativas, consultas parametrizadas y secretos fuera del repositorio.
El código de aplicación requiere autorización del líder, y toda rama se integra
mediante Pull Request con revisión.

3. Fase 1: modelo entidad-relación
3.1 Tablas por base de datos (primera versión)
security_db
usuarios : correo único, hash de la contraseña, nombre completo, teléfono, estado
activo y fechas.
roles y usuario_roles : relación de muchos a muchos entre usuarios y roles.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 1 of 11
tokens_refresco : guarda el hash del token, su expiración y su revocación.
registros_auditoria : acciones administrativas, con los detalles en JSONB.
catalog_db
marcas y familias_olfativas .
productos : marca, familia, nombre, slug, descripción, género, imagen y estado.
presentaciones : SKU único, tamaño en ml y precio en COP.
orders_db
direcciones , carritos (uno por usuario) e items_carrito .
pedidos : estado, total y copia de la dirección en columnas envio_* .
items_pedido : copia del producto (nombre, marca, tamaño y precio) al momento de
comprar.
pagos : relación uno a uno con el pedido.
3.2 Decisiones de diseño y su razón
Sin llaves foráneas entre bases: PostgreSQL no puede validar una llave hacia otra
base. Por eso usuario_id y presentacion_id son referencias lógicas: se guarda el
UUID y el servicio valida porAPI.
Snapshots en pedidos: si el usuario cambia su dirección o el catálogo cambia un
precio, el pedido conserva lo que realmente se compró. Por eso no hay relación entre
pedidos y direcciones .
Producto separado de presentación: el mismo perfume se vende en varios tamaños
con precios distintos, y así no se repite el nombre ni la descripción.
Restricciones únicas: UNIQUE (producto_id, tamano_ml) evita presentaciones
duplicadas, carritos.usuario_id limita a un carrito por usuario y pagos.pedido_id
garantiza la relación 1 a 1.
Seguridad en los datos: se guarda el hash de la contraseña y el hash del token, nunca
los valores reales.
Índices en las llaves foráneas y en usuario_id , para el historial y las consultas por
usuario.
3.3 Puntos abiertos que se llevaron al equipo
Si el carrito vive en el backend o en el navegador (ADR pendiente).
Si basta un rol por usuario o se mantiene la tabla intermedia.
Qué estados tendrá el pedido.
Si una familia olfativa es única por producto o puede haber varias.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 2 of 11
Si se manejan varias imágenes por producto.
La sección de mayoristas no tiene tablas, porque es solo «Próximamente».
3.4 Los diagramas en draw.io
Se usó la extensión Draw.io Integration de VS Code. Se creó un archivo por base ( ersecurity_db.drawio , er-catalog_db.drawio y er-orders_db.drawio ) y se exportó
un PNG de cada uno.
El código se pegó con Arrange → Insert → Advanced → Mermaid.
Notación de las líneas: 1 obligatorio a muchos opcional en casi todas las relaciones, 1 a
muchos obligatorio entre pedidos e items_pedido , y 1 a 1 entre pedidos y pagos .
Aclaración de conceptos: copia es un valor guardado tal como estaba al comprar, y
referencia lógica es un UUID que apunta a otra base sin llave foránea.
A pedido del equipo, los diagramas se pasaron a español, sin tildes ni eñes en los
nombres de tablas y columnas.
Se preparó un guion para exponer los tres ER, con las preguntas más probables y sus
respuestas.

4. Fase 2: entorno y creación física
4.1 Herramientas
VS Code con las extensiones SQLTools y el driver de PostgreSQL. La conexión se
configuró con «Ask on connect», para no guardar la contraseña.
Se evaluó SQLite, pero se descartó para los scripts oficiales: el README fija
PostgreSQL y los scripts usan UUID, TIMESTAMPTZ , JSONB y varias bases de datos.
Se instaló PostgreSQL en Windows. El instalador avisó que el directorio no estaba
vacío, y se resolvió eligiendo una carpeta nueva.
La conexión desde SQLTools se probó con el mensaje «Successfully connected!».
4.2 Scripts de creación ( Databases/init )
001_crear_bases_de_datos.sql , 002_security_db.sql , 003_catalog_db.sql y
004_orders_db.sql .
Se ejecutaron uno por uno con psql , con la opción ON_ERROR_STOP=1 para detenerse
ante cualquier error.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 3 of 11
4.3 Problemas y soluciones
psql no se reconocía: la carpeta bin de PostgreSQL no estaba en el PATH. Se
agregó, o se usó la ruta completa.
Los scripts no imprimían nada: los archivos estaban vacíos o sin guardar. Se resolvió
con Ctrl+S y comprobando con Get-Content .
Faltaban tablas en security_db : un error de sintaxis por un espacio dentro de un
nombre ( usuario_ id ) detuvo el script. Se corrigió el archivo y se recreó la base
desde cero.
Dos comandos pegados juntos: PowerShell mezclaba las contraseñas. Se ejecutan
uno a la vez.

5. Fase 3: primeras directivas de cambio
5.1 Sin stock
La primera directiva fue no manejar stock, por lo que la columna se quitó de
presentaciones . Más adelante la directiva se invirtió (ver sección 7).
5.2 Rol manager y permisos
Directiva: el manager controla y gestiona los paneles de la perfumería, pero no accede a
seguridad, configuración ni información sensible.
Se agregó el modelo de permisos: tablas permisos y rol_permisos .
Migración 001_agregar_manager_y_permisos.sql : crea esas dos tablas y renombra
admin_usuario_id a usuario_id en registros_auditoria , porque el manager
también queda auditado.
Permisos definidos: panel_local.acceder , catalogo.gestionar ,
pedidos.consultar , pedidos.gestionar , usuarios.gestionar ,
seguridad.acceder , configuracion.gestionar , auditoria.consultar y
datos_sensibles.consultar .
El manager tiene los primeros cuatro y el admin tiene los nueve. El cliente no necesita
permisos: accede solo a sus propios datos.
Aclaración: la base de datos solo registra los permisos. Quien los hace cumplir es el
backend, en el servidor.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 4 of 11
5.3 Estructura y datos por separado
Las migraciones solo cambian la estructura. Los datos (roles, permisos y asignaciones)
pasaron a los seeds 001_roles.sql y 003_permisos.sql . El orden de ejecución quedó
fijado: la migración primero y el seed después.

6. Fase 4: datos iniciales (seeds)
Primero se hicieron datos de prueba para todas las tablas. Al cerrar las pruebas se
pidió dejar inserts definitivos.
Seed 002_catalogo.sql : 6 marcas, 6 familias olfativas, 30 productos y 90
presentaciones (30, 50 y 100 ml) con precios de referencia en COP.
Las marcas y los nombres de perfumes son inventados, sin marcas existentes, y se
reemplazarán tras el visto bueno del equipo.
Se decidió no incluir usuarios, carritos ni pedidos: los genera el sistema, y un usuario
necesita un hash de contraseña real que no debe estar en el repositorio.
Se explicó cuándo sí convendría un archivo aparte de pedidos de demostración, solo
para el entorno de demo.

7. Fase 5: el stock vuelve al modelo
Una directiva posterior ordenó manejar stock. Se creó una tabla aparte:
inventario : una fila por presentación ( presentacion_id como llave primaria y
foránea), cantidad con CHECK (cantidad >= 0) y actualizado_en .
Migración 002_agregar_inventario.sql y seed 004_inventario.sql : 90 filas con
cantidades entre 10 y 50 unidades, repartidas con una fórmula fija.
Se entregaron 11 consultas SQL de stock, con parámetros para evitar inyección SQL:
catálogo con filtros, detalle de producto, revalidación en el checkout, descuento
atómico, reposición, fijar stock, stock bajo, agotados, resumen por marca y creación
de una presentación junto con su stock.
El descuento se hace como una sola operación ( UPDATE ... WHERE cantidad >= n ),
para que dos compras simultáneas no dejen el stock en negativo.
Quedó abierto si cancelar un pedido devuelve unidades al stock.

8. Fase 6: calidad AAA
Definición recibida: AAA identifica réplicas de mayor similitud estética frente a copias
básicas.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 5 of 11
Se decidió una tabla de calidades en lugar de duplicar productos , presentaciones e
inventario : calidades y la columna productos.calidad_id .
Migración 003_agregar_calidades.sql y seed 005_calidades.sql , con las
calidades AAA y BASICA . La asignación a los productos es provisional: 15 productos
AAA (las marcas 3, 4 y 5) y 15 BASICA.
Redundancia: el equipo señaló que codigo y nombre guardaban casi lo mismo. Se
eliminó la columna nombre , y quedaron id , codigo y descripcion . El seed pasó a
usar ON CONFLICT DO UPDATE para refrescar la descripción.
Para aplicar el cambio en la base local se borró y recreó la tabla (primero la columna
calidad_id y luego calidades ) y se volvió a ejecutar la migración y el seed.
Riesgo señalado: las réplicas con marcas registradas pueden infringir derechos de
marca. Se recomendó no usar marcas reales ni la palabra «originales», mantener la
etiqueta visible y honesta, no guardar la marca original y confirmar el enfoque con el
líder.

9. Incidentes de entorno y de Git
9.1 Contraseña de postgres
Se perdió la clave del servidor local. Solución, sin perder datos:
1. Cambiar temporalmente a trust las dos líneas host de pg_hba.conf .
2. Reiniciar el servicio.
3. Entrar con psql y usar \password postgres .
4. Devolver las líneas a scram-sha-256 y reiniciar otra vez, para no dejar la base abierta.
9.2 Ramas y Pull Requests
La rama original se borró en GitHub tras unirse un PR, y el PR #7 se había revertido. El
comando git pull fallaba con couldn't find remote ref .
El historial de main mostró un revert unido y ramas desalineadas, con una
advertencia de multiple merge bases . Por eso no se hizo git merge sobre la rama
vieja.
Se aplicó el método limpio: una rama nueva desde main y git checkout rama-vieja
-- Databases para traer solo la carpeta de base de datos.
Un revisor comentó el archivo seeds/001_roles.sql . Se comprobó que el SQL se
ejecutaba sin errores y se revisó el historial: el problema estaba en la rama y no en el
texto de la sentencia.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 6 of 11
Se explicó cómo hacer un commit de solo algunos archivos, con git add de rutas
concretas.
9.3 Otros avisos
El aviso de saltos de línea LF/CRLF es normal en Windows y no afecta.
Se eliminaron los .gitkeep de las carpetas que ya tenían archivos reales.
Se detectó un merge a medias ( All conflicts fixed but you are still
merging ), en el que git commit parcial no es posible. Se explicaron las dos salidas:
abortar y trabajar desde una rama limpia, o concluir el merge.
Se advirtió que node_modules estaba dentro del repositorio, algo que debe
corregirse en un PR aparte.

10. Fase 7: revisión técnica del equipo y correcciones
El equipo entregó un informe de inconsistencias. Estos fueron los puntos y su
tratamiento.
Dos fuentes de verdad para security_db : los scripts de Databases/init y la
migración Alembic del servicio de seguridad. Recomendación: que Alembic sea el
dueño, tras comprobar que incluya permisos , rol_permisos y usuario_id en la
auditoría.
Migraciones mixtas: Alembic solo cubre el servicio de seguridad, y catálogo y
pedidos dependen de SQL manual, sin tabla de versiones.
Roles con tres nombres: cliente , customer y la lista del ER. Recomendación:
customer , manager y admin , porque el JWT y el ADR-0009 ya usan customer .
Estados del pedido: el script permitía solo pagado_simulado y cancelado , y las
reglas de negocio piden paid , preparing , shipped y delivered .
ADR-0004 abierto: Prisma instalado sin schema.prisma y sin dueño definido para
catálogo y pedidos.
Documentación desactualizada: el README apuntaba a rutas antiguas de los ER, y
architecture.md nombraba tablas que no existen ( products , product_variants ,
audit_events , order_addresses y order_status_history ).
Cambios sin integrar: inventario y calidades estaban en la rama del compañero y no
en main .
Detalles de formalización: TIMESTAMP sin zona en seguridad, tamano_ml > 0 en vez
de 30, 50 y 100, y solo un contenedor de base de datos en docker-compose .
Lo que está bien: los snapshots de pedido y las referencias lógicas sin llave foránea
son decisiones intencionales y están documentadas.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 7 of 11
10.1 Equivalencias entre la documentación y la base real
products corresponde a productos .
product_variants corresponde a presentaciones .
audit_events corresponde a registros_auditoria .
order_addresses corresponde a las columnas envio_* de pedidos , que son una
copia y no una tabla.
order_status_history no existe, y queda por decidir si se crea.
10.2 Migración 004: estados del pedido
Se reescribió para depender del nombre exacto de la restricción
( pedidos_estado_check ), no de una búsqueda por texto, para evitar borrar una
restricción equivocada.
Va dentro de una transacción ( BEGIN y COMMIT ): si algo falla, no se aplica nada.
Convierte pagado_simulado en paid y cancelado en cancelled , cambia el valor
por defecto a paid y fija la restricción con paid , preparing , shipped , delivered y
cancelled .
Se verificó el nombre con \d pedidos antes de ejecutarla. La salida fue BEGIN ,
ALTER TABLE , UPDATE 0 (dos veces, porque no hay pedidos), dos ALTER TABLE y
COMMIT , y la tabla quedó con el valor por defecto paid y la restricción nueva.
10.3 Migración 005: tamaños de presentación
Sustituye la restricción tamano_ml > 0 por tamano_ml IN (30, 50, 100) , con la
misma técnica: nombre exacto y transacción.
Se verificó que la restricción existente se llamaba presentaciones_tamano_ml_check .
Falta registrar la salida de su ejecución.
10.4 Correcciones en los ER
catalog_db : la segunda tabla estaba rotulada productos y debe llamarse
presentaciones ; se agregan inventario y calidades .
security_db : usuario_id en lugar de admin_usuario_id , y las tablas permisos y
rol_permisos .
orders_db : corregir nombre_destinario por nombre_destinatario y actualizar los
estados del pedido.
Los tres diagramas corregidos se mostraron en imagen para llevarlos a los archivos
.drawio de docs/diagrams .
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 8 of 11

11. Estado final de la base de datos
11.1 Tablas
security_db (7): usuarios , roles , usuario_roles , permisos , rol_permisos ,
tokens_refresco y registros_auditoria .
catalog_db (6): marcas , familias_olfativas , calidades , productos ,
presentaciones e inventario .
orders_db (6): direcciones , carritos , items_carrito , pedidos , items_pedido
y pagos .
11.2 Datos esperados
3 roles, 9 permisos y 13 asignaciones (manager con 4 y admin con 9).
6 marcas, 6 familias, 30 productos y 90 presentaciones.
90 filas de inventario, entre 10 y 50 unidades.
Calidades: 15 productos AAA y 15 BASICA.
11.3 Orden de ejecución desde cero
1. init/001 a init/004 .
2. migrations/001 , 002 , 003 , 004 y 005 .
3. seeds/001_roles , 002_catalogo , 003_permisos , 004_inventario y
005_calidades .
Cada archivo se ejecuta uno por uno, con el archivo guardado:
psql -U postgres -v ON_ERROR_STOP=1 -f Databases/init/002_security_db.sql
11.4 Comandos de verificación
Bases creadas y tablas por base:
psql -U postgres -c "\l"
psql -U postgres -d security_db -c "\dt"
psql -U postgres -d catalog_db -c "\dt"
psql -U postgres -d orders_db -c "\dt"
Roles y permisos:
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 9 of 11
psql -U postgres -d security_db -c "SELECT (SELECT count(*) FROM roles) AS
roles, (SELECT count(*) FROM permisos) AS permisos, (SELECT count(*) FROM
rol_permisos) AS rol_permisos;"
psql -U postgres -d security_db -c "SELECT r.nombre AS rol, COUNT(*) AS
permisos FROM rol_permisos rp JOIN roles r ON r.id = rp.rol_id GROUP BY
r.nombre;"
psql -U postgres -d security_db -c "\d registros_auditoria"
Catálogo, inventario y calidades:
psql -U postgres -d catalog_db -c "SELECT (SELECT count(*) FROM marcas) AS
marcas, (SELECT count(*) FROM familias_olfativas) AS familias, (SELECT
count(*) FROM productos) AS productos, (SELECT count(*) FROM presentaciones)
AS presentaciones;"
psql -U postgres -d catalog_db -c "SELECT count(*) AS filas, min(cantidad) AS
minimo, max(cantidad) AS maximo FROM inventario;"
psql -U postgres -d catalog_db -c "SELECT c.codigo, count(*) AS productos
FROM productos p JOIN calidades c ON c.id = p.calidad_id GROUP BY c.codigo
ORDER BY c.codigo;"
psql -U postgres -d catalog_db -c "\d presentaciones"
Estados del pedido y comprobación de archivos y Git:
psql -U postgres -d orders_db -c "\d pedidos"
Get-Content Databases/seeds/003_permisos.sql
git status
git fetch --prune
git log --oneline origin/main..HEAD
git diff --check origin/main...HEAD

12. Pendientes y decisiones del equipo
Confirmar la salida de la migración 005 y su prueba de rechazo de un tamaño no
permitido.
Integrar a main el inventario, las calidades y los seeds 004 y 005, en su versión
corregida (calidades sin la columna nombre ).
Pasar a los archivos .drawio los tres ER corregidos y actualizar las rutas del README
a docs/diagrams/ .
Decidir el nombre de los roles ( cliente o customer ) y actualizar seeds, ER y
documentación.
Decidir quién es dueño de security_db (Alembic o los scripts) y conciliar TIMESTAMP
y el DEFAULT del UUID.
Informe del trabajo en la base de datos de PerfumesPAYDAY
Page 10 of 11
Cerrar el ADR-0004 con una sola herramienta para cambiar el esquema de catálogo y
pedidos, y una tabla de versiones de migraciones.
Agregar los contenedores de catalog_db y orders_db a docker-compose .
Decidir si cancelar un pedido devuelve stock, y si se crea una tabla de historial de
estados.
Sustituir las marcas provisionales por las reales tras el visto bueno, y definir la
clasificación AAA real de cada producto.
Confirmar con el líder o el profesor el enfoque de las réplicas por el riesgo de marcas
registradas.
Quitar node_modules del control de Git, en un PR aparte.

13. Commits sugeridos
feat(database): esquema de las tres bases de datos
feat(database): rol manager, permisos e inventario
feat(database): agregar tabla de calidades y clasificar productos AAA
feat(database): alinear estados de pedido y tamanos de presentacion
feat(database): seeds de roles, catalogo, permisos, inventario y calidades
docs(diagrams): corregir ER de security, catalog y orders
## Tecnologías
- PostgreSQL
- Prisma / Drizzle (por definir)
