\connect catalog_db

-- Calidades: el codigo identifica la gama y la descripcion la explica
INSERT INTO calidades (codigo, descripcion) VALUES
    ('AAA',    'Replica de alta similitud estetica'),
    ('BASICA', 'Copia de similitud estetica basica')
ON CONFLICT (codigo) DO UPDATE SET descripcion = EXCLUDED.descripcion;

-- Asignacion provisional: las marcas 3, 4 y 5 quedan como AAA y el resto como BASICA.
-- Es un marcador, el equipo debe definir la calidad real de cada producto.
UPDATE productos p
SET calidad_id = c.id
FROM calidades c, marcas m
WHERE m.id = p.marca_id
  AND c.codigo = CASE WHEN m.slug IN ('maison-alcor', 'essencia-valdor', 'perfumeria-orvano')
                      THEN 'AAA' ELSE 'BASICA' END;