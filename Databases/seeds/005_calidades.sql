\connect catalog_db

INSERT INTO calidades (codigo, nombre, descripcion) VALUES
    ('AAA',    'Triple AAA', 'Replica de alta similitud estetica'),
    ('BASICA', 'Basica',     'Copia basica')
ON CONFLICT (codigo) DO NOTHING;

-- Asignacion provisional: las marcas 3, 4 y 5 quedan como AAA y el resto como BASICA.
-- Es un marcador, el equipo debe definir la calidad real de cada producto.
UPDATE productos p
SET calidad_id = c.id
FROM calidades c, marcas m
WHERE m.id = p.marca_id
  AND c.codigo = CASE WHEN m.slug IN ('maison-alcor', 'essencia-valdor', 'perfumeria-orvano')
                      THEN 'AAA' ELSE 'BASICA' END;