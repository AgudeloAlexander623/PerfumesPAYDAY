# CU-16 — Gestionar direcciones de envío

| Campo | Valor |
|---|---|
| Módulo | Checkout y direcciones |
| Actores | Cliente (principal), order-service (sistema) |
| Prioridad | Must |
| Diagrama | [`06-direcciones-checkout`](../diagrams/06-direcciones-checkout.svg) |

## Objetivo

Permitir que el cliente cree, consulte, edite y elimine sus direcciones de envío, y elija una como predeterminada.

## Precondiciones

- El usuario tiene una sesión activa.

## Disparador

El usuario abre **Mis direcciones** desde su perfil o desde el checkout.

## Flujo principal

1. El usuario abre la lista de direcciones.
2. El frontend solicita las direcciones al gateway.
3. El gateway enruta a `order-service` y toma el `user_id` del token.
4. `order-service` devuelve solo las direcciones de ese usuario.
5. El frontend muestra la lista e indica cuál es la predeterminada.

## Subflujos

### S1 — Crear dirección

1. El usuario selecciona **Agregar dirección**.
2. Ingresa nombre de quien recibe, teléfono, departamento, ciudad, dirección y referencias.
3. El frontend valida los campos obligatorios.
4. `order-service` valida los datos y guarda la dirección asociada al `user_id`.
5. Si es la primera dirección, queda como predeterminada.

### S2 — Editar dirección

1. El usuario selecciona **Editar**.
2. Modifica los campos permitidos y guarda.
3. `order-service` verifica que la dirección pertenezca al usuario y actualiza los datos.

### S3 — Marcar como predeterminada

1. El usuario selecciona **Usar como predeterminada**.
2. `order-service` quita la marca de la anterior y la asigna a la nueva en una sola operación.

### S4 — Eliminar dirección

1. El usuario selecciona **Eliminar** y confirma.
2. `order-service` verifica la pertenencia y elimina la dirección.
3. Si era la predeterminada, el usuario elige otra o queda sin predeterminada.

## Flujos alternativos

### A1 — Datos inválidos

- **Cuándo ocurre:** falta un campo, el teléfono tiene formato incorrecto o el departamento no existe.
- **Respuesta del sistema:** responde `400` o `422` con los campos a corregir.

### A2 — Dirección de otro usuario

- **Cuándo ocurre:** se intenta editar o eliminar una dirección ajena.
- **Respuesta del sistema:** responde `404` sin confirmar que existe.

### A3 — Límite de direcciones alcanzado

- **Cuándo ocurre:** el usuario supera el máximo permitido.
- **Respuesta del sistema:** responde `409` y pide eliminar una dirección antes de crear otra.

### A4 — Dirección usada en un pedido

- **Cuándo ocurre:** se elimina una dirección que ya fue usada en una compra.
- **Respuesta del sistema:** la eliminación se permite; el pedido conserva su propia copia de los datos.

### A5 — Servicio no disponible

- **Cuándo ocurre:** `order-service` no responde.
- **Respuesta del sistema:** responde `503` y conserva los datos ingresados en el formulario.

## Postcondiciones

- Las direcciones quedan asociadas al usuario autenticado.
- Existe como máximo una dirección predeterminada por usuario.
- Los pedidos anteriores no cambian al editar o eliminar una dirección.

## Reglas de negocio

- Cada usuario solo ve y modifica sus propias direcciones.
- Solo puede haber una dirección predeterminada.
- El departamento y la ciudad se validan contra la lista de Colombia.
- El teléfono se guarda como texto, no como número, para conservar ceros y prefijos.
- Las direcciones se guardan en `orders_db` porque pertenecen al dominio de pedidos.
- Los pedidos guardan una copia de la dirección usada; no dependen de la dirección actual.

## Datos y servicios involucrados

- **Servicio:** `order-service`.
- **Base de datos:** `orders_db`.
- **Entidad:** `addresses` con `id`, `user_id`, `recipient_name`, `phone`, `department`, `city`, `address_line`, `references`, `is_default`, `created_at`, `updated_at`.

## Seguridad

- El `user_id` se toma del token.
- Toda consulta filtra por `user_id` para evitar IDOR.
- Se responde `404` ante recursos ajenos.
- Los datos personales no se escriben en logs.
- Se valida el tamaño y el tipo de cada campo.

## Criterios de aceptación

- [ ] El usuario puede crear, listar, editar y eliminar sus direcciones.
- [ ] Solo puede existir una dirección predeterminada.
- [ ] Una dirección ajena devuelve `404`.
- [ ] Los datos inválidos devuelven `400` o `422`.
- [ ] Eliminar una dirección no altera pedidos anteriores.
- [ ] La primera dirección queda como predeterminada.
