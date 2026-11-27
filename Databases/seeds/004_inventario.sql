\connect catalog_db

INSERT INTO inventario (presentacion_id, cantidad)
SELECT id, 10 + ((row_number() OVER (ORDER BY sku)) * 7) % 41
FROM presentaciones
ON CONFLICT DO NOTHING;