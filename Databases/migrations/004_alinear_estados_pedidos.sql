\connect orders_db

-- Alinea los estados del pedido con docs/business-rules.md:
-- paid -> preparing -> shipped -> delivered (y cancelled).
-- Ejecutar UNA sola vez. Todo va en una transaccion: si algo falla, no se aplica nada.
-- Antes de correrla, confirmar el nombre de la restriccion con:  \d pedidos

BEGIN;

-- 1. Quitar la restriccion actual del estado, por su nombre exacto.
--    Si el nombre no existe, el script falla y no cambia nada.
ALTER TABLE pedidos DROP CONSTRAINT pedidos_estado_check;

-- 2. Convertir los pedidos existentes a los codigos nuevos
UPDATE pedidos SET estado = 'paid'      WHERE estado = 'pagado_simulado';
UPDATE pedidos SET estado = 'cancelled' WHERE estado = 'cancelado';

-- 3. Nuevo valor por defecto y nueva restriccion.
--    Si quedara algun pedido con un estado inesperado, esta linea falla y se revierte todo.
ALTER TABLE pedidos ALTER COLUMN estado SET DEFAULT 'paid';
ALTER TABLE pedidos ADD CONSTRAINT pedidos_estado_check
    CHECK (estado IN ('paid', 'preparing', 'shipped', 'delivered', 'cancelled'));

COMMIT;