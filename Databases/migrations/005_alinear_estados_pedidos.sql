\connect catalog_db

-- Las presentaciones validas son 30, 50 y 100 ml (README y business-rules).
-- Ejecutar UNA sola vez. Todo va en una transaccion: si algo falla, no se aplica nada.
-- Antes de correrla, confirmar el nombre de la restriccion con:  \d presentaciones

BEGIN;

-- 1. Quitar la restriccion actual (tamano_ml > 0), por su nombre exacto
ALTER TABLE presentaciones DROP CONSTRAINT presentaciones_tamano_ml_check;

-- 2. Nueva restriccion. Si existiera una presentacion con otro tamano, falla y se revierte todo.
ALTER TABLE presentaciones ADD CONSTRAINT presentaciones_tamano_ml_check
    CHECK (tamano_ml IN (30, 50, 100));

COMMIT;