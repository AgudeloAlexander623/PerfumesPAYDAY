# Historias técnicas (habilitadoras) — PerfumesPAYDAY

> **Estado:** borrador 0.1 — pendiente de validación con el equipo.
> **Última actualización:** 2026-11-11
> **Fuente de verdad del comportamiento:** [`../use-cases/`](../use-cases/README.md). Estas historias no cambian el comportamiento funcional: habilitan que las historias de usuario se puedan construir, integrar, desplegar y aprobar.
> **Documentos relacionados:** [`../user-stories/`](../user-stories/user-stories.md) (historias de usuario), [`scrum.md`](scrum.md) (sprints y DoD), [`../beta-criteria.md`](../beta-criteria.md) (criterios de aceptación).

---

## 1. Qué es una historia técnica

Una **historia técnica** (o *habilitadora*) no la "ve" un usuario: describe trabajo de infraestructura, integración, datos o calidad que el **equipo de desarrollo** necesita para que las historias de usuario funcionen y cumplan los criterios de la beta.

En este proyecto son especialmente importantes porque:

1. La arquitectura obligatoria es de **microservicios**: sin entorno, gateway y contratos, nada se comunica.
2. La beta tiene una **prueba de hacking ético**: rate limit, CORS, autorización y secretos son requisitos evaluados, no extras.
3. La beta exige **despliegue con HTTPS**: sin eso no hay demo ni evaluación.

**Sin estas historias, las funcionales no se pueden construir ni aprobar.**

---

## 2. Formato

Igual que las historias de usuario, pero con el **equipo** como actor:

**Como** equipo, **quiero** *[capacidad técnica]*, **para** *[beneficio para el proyecto]*.

Con criterios de aceptación en formato **Dado / Cuando / Entonces**, verificables.

---

## 3. Índice de historias técnicas

| ID | Historia | Área | Semana |
|---|---|---|---|
| HT-01 | Levantar el entorno local con `docker-compose` | Infraestructura | 1 |
| HT-02 | Seed idempotente de productos | Datos | 2 |
| HT-03 | Rate limit en login, registro y checkout | Seguridad | 3 |
| HT-04 | CORS, cabeceras de seguridad y servicios internos sin exposición | Seguridad | 3 |
| HT-05 | Despliegue con HTTPS en URL pública | Infraestructura | 1 y 3 |
| HT-06 | Validación de rol y propiedad en el servidor | Seguridad | 1 |
| HT-07 | Integración continua en GitHub Actions | Calidad | 1 |
| HT-08 | Gateway como único punto de entrada y enrutamiento `/api/v1` | Integración | 1 |
| HT-09 | Contratos OpenAPI definidos y publicados antes de implementar | Integración | 1 |
| HT-10 | Prisma y migraciones de las tres bases de datos | Datos | 1 |
| HT-11 | Paquete compartido y configuración del monorepo | Integración | 1 |
| HT-12 | Manejo estándar de errores (ADR-0006) | Integración | 1 |
| HT-13 | Registro de eventos sin datos sensibles | Seguridad | 2 |
| HT-14 | Gestión de secretos fuera del repositorio | Seguridad | 1 |
| HT-15 | Arnés de pruebas y cobertura mínima | Calidad | 1 |

**Total: 15 historias técnicas** (las 7 originales, ampliadas con 8 habilitadores que el proyecto aún no cubría).

---

## 4. Infraestructura y entorno

### HT-01 · Levantar el entorno local con `docker-compose`
*Semana 1*

**Como** equipo, **quiero** levantar todo el entorno local con `docker-compose`, **para** que cualquiera ejecute el proyecto sin pasos manuales.

**Criterios de aceptación**

- **Dado** un equipo con Docker instalado, **cuando** ejecuto `docker compose up`, **entonces** se levantan los servicios y las bases de datos.
- **Dado** el entorno levantado, **cuando** consulto la salud de cada servicio, **entonces** responden correctamente.
- **Dado** que detengo el entorno, **cuando** lo vuelvo a levantar, **entonces** los datos persistidos se conservan.

---

### HT-05 · Despliegue con HTTPS en URL pública
*Semana 1 (inicial) y 3 (final)*

**Como** equipo, **quiero** desplegar la beta con HTTPS en una URL pública, **para** poder hacer la demo y la prueba del profesor.

**Criterios de aceptación**

- **Dado** el despliegue, **cuando** abro la URL pública, **entonces** responde por HTTPS.
- **Dado** que accedo a un servicio interno o a PostgreSQL desde internet, **cuando** lo intento, **entonces** no es accesible.
- **Dado** que actualizo la versión desplegada, **cuando** termina el despliegue, **entonces** la URL sigue respondiendo.

---

### HT-14 · Gestión de secretos fuera del repositorio
*Semana 1*

**Como** equipo, **quiero** mantener los secretos fuera del repositorio, **para** no filtrar claves ni credenciales.

**Criterios de aceptación**

- **Dado** el repositorio, **cuando** lo reviso, **entonces** solo contiene `.env.example` y ningún `.env` real ni claves.
- **Dado** que un servicio necesita un secreto, **cuando** arranca, **entonces** lo lee de una variable de entorno.
- **Dado** que un secreto falta, **cuando** el servicio arranca, **entonces** falla con un mensaje claro y no con un valor por defecto inseguro.

---

## 5. Integración y contratos

### HT-08 · Gateway como único punto de entrada y enrutamiento `/api/v1`
*Semana 1*

**Como** equipo, **quiero** que el gateway sea el único punto de entrada y enrute por `/api/v1`, **para** centralizar el acceso y ocultar los servicios internos.

**Criterios de aceptación**

- **Dado** una petición del frontend, **cuando** llega al gateway, **entonces** se enruta al servicio correcto.
- **Dado** una ruta inexistente, **cuando** llega al gateway, **entonces** responde con el formato de error estándar.
- **Dado** un servicio interno, **cuando** intento accederlo directamente desde internet, **entonces** no es accesible.

---

### HT-09 · Contratos OpenAPI definidos y publicados antes de implementar
*Semana 1*

**Como** equipo, **quiero** definir y publicar los contratos OpenAPI antes de implementar, **para** que frontend y backend trabajen contra el mismo acuerdo.

**Criterios de aceptación**

- **Dado** un endpoint nuevo, **cuando** empieza su implementación, **entonces** su contrato OpenAPI ya está definido (método, ruta, entrada, salida y errores).
- **Dado** el contrato, **cuando** lo consulto, **entonces** está publicado en `docs/api/`.
- **Dado** un cambio de contrato, **cuando** se integra, **entonces** se actualiza en el mismo pull request.

---

### HT-11 · Paquete compartido y configuración del monorepo
*Semana 1*

**Como** equipo, **quiero** un paquete compartido y una configuración única del monorepo, **para** no duplicar utilidades ni configuración entre servicios.

**Criterios de aceptación**

- **Dado** el workspace, **cuando** instalo dependencias, **entonces** todos los servicios comparten la configuración base de TypeScript.
- **Dado** un tipo o utilidad común, **cuando** lo necesito, **entonces** lo importo desde `@perfumespayday/shared` en lugar de reescribirlo.
- **Dado** el repositorio, **cuando** compilo, **entonces** los servicios compilan sin errores de tipos.

---

### HT-12 · Manejo estándar de errores
*Semana 1 · Depende de [ADR-0006](../adr/0006-errores-paginacion-idempotencia.md)*

**Como** equipo, **quiero** un formato único de errores, paginación e idempotencia, **para** que todos los servicios respondan igual.

**Criterios de aceptación**

- **Dado** un error en cualquier servicio, **cuando** llega al cliente, **entonces** usa el formato estándar definido en ADR-0006.
- **Dado** un error, **cuando** se muestra, **entonces** no expone trazas, rutas ni detalles internos.
- **Dado** un listado paginado, **cuando** lo consulto, **entonces** usa la convención de paginación acordada.

---

## 6. Datos

### HT-10 · Prisma y migraciones de las tres bases de datos
*Semana 1 · Depende de [ADR-0004](../adr/0004-propiedad-datos.md)*

**Como** equipo, **quiero** gestionar los modelos y migraciones con Prisma, **para** crear y versionar las tablas de las tres bases de datos.

**Criterios de aceptación**

- **Dado** el esquema de cada base, **cuando** aplico las migraciones, **entonces** las tablas se crean según los scripts SQL existentes.
- **Dado** un cambio de modelo, **cuando** genero una migración, **entonces** queda versionada en el repositorio.
- **Dado** un servicio, **cuando** accede a datos, **entonces** usa solo su propia base (sin tablas compartidas).

---

### HT-02 · Seed idempotente de productos
*Semana 2*

**Como** equipo, **quiero** un *seed* idempotente, **para** cargar los 25 a 30 productos de demostración sin duplicarlos.

**Criterios de aceptación**

- **Dado** el *seed*, **cuando** lo ejecuto una vez, **entonces** carga los productos, marcas y presentaciones.
- **Dado** que lo ejecuto dos veces, **cuando** termina, **entonces** los datos son los mismos (sin duplicados).
- **Dado** el catálogo cargado, **cuando** lo consulto, **entonces** muestra productos con presentaciones de 30, 50 y 100 ml.

---

## 7. Seguridad

### HT-03 · Rate limit en login, registro y checkout
*Semana 3*

**Como** equipo, **quiero** *rate limit* en login, registro y checkout, **para** frenar abusos y fuerza bruta.

**Criterios de aceptación**

- **Dado** un usuario que supera el límite de intentos, **cuando** insiste, **entonces** recibe un bloqueo temporal (`429`).
- **Dado** el límite configurado, **cuando** se alcanza, **entonces** se aplica por usuario e IP.
- **Dado** el checkout, **cuando** se repite demasiado, **entonces** se limita sin afectar la idempotencia.

---

### HT-04 · CORS, cabeceras de seguridad y servicios internos sin exposición
*Semana 3*

**Como** equipo, **quiero** CORS con lista de orígenes permitidos y cabeceras de seguridad, **para** reducir la superficie de ataque.

**Criterios de aceptación**

- **Dado** un origen no permitido, **cuando** hace una petición, **entonces** CORS la rechaza.
- **Dado** una respuesta, **cuando** la inspecciono, **entonces** incluye las cabeceras de seguridad configuradas.
- **Dado** los servicios internos y PostgreSQL, **cuando** intento accederlos desde internet, **entonces** no están expuestos.

---

### HT-06 · Validación de rol y propiedad en el servidor
*Semana 1*

**Como** equipo, **quiero** validar el rol y la propiedad de los recursos en el servidor, **para** que ocultar un botón no sea la única protección.

**Criterios de aceptación**

- **Dado** un `cliente`, **cuando** intenta una acción de administración, **entonces** recibe `403`.
- **Dado** un `cliente`, **cuando** intenta acceder a un recurso ajeno, **entonces** recibe `404`.
- **Dado** el `user_id`, **cuando** se usa, **entonces** siempre sale del token y nunca del cuerpo o la URL.

---

### HT-13 · Registro de eventos sin datos sensibles
*Semana 2*

**Como** equipo, **quiero** registrar eventos sin datos sensibles, **para** depurar y auditar sin filtrar información personal.

**Criterios de aceptación**

- **Dado** un error o una acción relevante, **cuando** se registra, **entonces** el log no incluye contraseñas, tokens ni datos personales.
- **Dado** un evento de auditoría, **cuando** se guarda, **entonces** es *append-only* y con fecha ISO 8601 UTC.
- **Dado** un log, **cuando** lo reviso, **entonces** permite reconstruir qué pasó sin exponer secretos.

---

## 8. Calidad

### HT-07 · Integración continua en GitHub Actions
*Semana 1*

**Como** equipo, **quiero** integración continua en GitHub Actions, **para** validar cada cambio antes de integrarlo.

**Criterios de aceptación**

- **Dado** un pull request, **cuando** se abre o actualiza, **entonces** se ejecutan *lint* y pruebas.
- **Dado** que alguna comprobación falla, **cuando** se intenta integrar, **entonces** el *merge* se bloquea.
- **Dado** un cambio integrado en `main`, **cuando** termina el *pipeline*, **entonces** queda en verde.

---

### HT-15 · Arnés de pruebas y cobertura mínima
*Semana 1*

**Como** equipo, **quiero** un arnés de pruebas con cobertura mínima, **para** que los criterios de aceptación tengan respaldo automático.

**Criterios de aceptación**

- **Dado** el proyecto, **cuando** ejecuto las pruebas, **entonces** corren en local y en CI con un solo comando.
- **Dado** un criterio de seguridad o idempotencia, **cuando** se implementa, **entonces** tiene una prueba automática.
- **Dado** el reporte de cobertura, **cuando** lo consulto, **entonces** muestra el porcentaje por servicio.

---

## 9. Relación con las historias de usuario

- Las historias técnicas **no** sustituyen a las de usuario; las **habilitan**.
- Varias son **prerequisito** de los sprints: HT-01, HT-05, HT-06, HT-07, HT-08, HT-09, HT-10, HT-11, HT-12, HT-14 y HT-15 deben avanzar en el **Sprint 1** para que las funcionales del Sprint 1 y 2 sean construibles.
- En el tablero se etiquetan como `tipo:ht` y viven en la swimlane de su área.

---

**Versión:** 0.1
**Responsable:** Product Owner
