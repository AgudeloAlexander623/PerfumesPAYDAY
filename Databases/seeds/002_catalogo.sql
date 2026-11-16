\connect catalog_db

-- =====================================================
-- Marcas (nombres provisionales; se reemplazan tras el visto bueno)
-- =====================================================
INSERT INTO marcas (nombre, slug) VALUES
    ('Casa Nebula',       'casa-nebula'),
    ('Atelier Brumar',    'atelier-brumar'),
    ('Maison Alcor',      'maison-alcor'),
    ('Essencia Valdor',   'essencia-valdor'),
    ('Perfumeria Orvano', 'perfumeria-orvano'),
    ('Aromas Lumbre',     'aromas-lumbre')
ON CONFLICT DO NOTHING;

INSERT INTO familias_olfativas (nombre) VALUES
    ('Citrica'), ('Floral'), ('Amaderada'), ('Oriental'), ('Acuatica'), ('Aromatica')
ON CONFLICT DO NOTHING;

-- =====================================================
-- Catalogo base (tabla temporal usada por los dos INSERT siguientes)
-- precio_30 = precio de referencia de 30 ml en COP
-- =====================================================
CREATE TEMP TABLE tmp_catalogo AS
SELECT * FROM (VALUES
    ('001', 'casa-nebula',       'Citrica',   'Alba Dorada',      'alba-dorada',      'unisex',  95000),
    ('002', 'casa-nebula',       'Acuatica',  'Brisa Marina',     'brisa-marina',     'hombre',  90000),
    ('003', 'casa-nebula',       'Floral',    'Jardin Secreto',   'jardin-secreto',   'mujer',  105000),
    ('004', 'casa-nebula',       'Amaderada', 'Madera Noble',     'madera-noble',     'hombre', 110000),
    ('005', 'casa-nebula',       'Oriental',  'Ambar Lunar',      'ambar-lunar',      'unisex', 120000),
    ('006', 'atelier-brumar',    'Acuatica',  'Niebla Fresca',    'niebla-fresca',    'unisex',  85000),
    ('007', 'atelier-brumar',    'Floral',    'Rosa Eterna',      'rosa-eterna',      'mujer',  100000),
    ('008', 'atelier-brumar',    'Amaderada', 'Cedro Ahumado',    'cedro-ahumado',    'hombre', 115000),
    ('009', 'atelier-brumar',    'Oriental',  'Vainilla Nocturna','vainilla-nocturna','mujer',  125000),
    ('010', 'atelier-brumar',    'Citrica',   'Limon Sereno',     'limon-sereno',     'unisex',  80000),
    ('011', 'maison-alcor',      'Floral',    'Flor de Luna',     'flor-de-luna',     'mujer',  130000),
    ('012', 'maison-alcor',      'Amaderada', 'Roble Intenso',    'roble-intenso',    'hombre', 135000),
    ('013', 'maison-alcor',      'Oriental',  'Especia Real',     'especia-real',     'unisex', 140000),
    ('014', 'maison-alcor',      'Citrica',   'Pomelo Rosado',    'pomelo-rosado',    'mujer',  100000),
    ('015', 'maison-alcor',      'Aromatica', 'Hierba Alta',      'hierba-alta',      'hombre',  95000),
    ('016', 'essencia-valdor',   'Aromatica', 'Lavanda Plena',    'lavanda-plena',    'unisex',  90000),
    ('017', 'essencia-valdor',   'Acuatica',  'Oceano Claro',     'oceano-claro',     'hombre',  95000),
    ('018', 'essencia-valdor',   'Floral',    'Peonia Blanca',    'peonia-blanca',    'mujer',  110000),
    ('019', 'essencia-valdor',   'Amaderada', 'Sandalo Calido',   'sandalo-calido',   'unisex', 125000),
    ('020', 'essencia-valdor',   'Oriental',  'Incienso Oro',     'incienso-oro',     'unisex', 150000),
    ('021', 'perfumeria-orvano', 'Citrica',   'Naranja Amarga',   'naranja-amarga',   'unisex',  85000),
    ('022', 'perfumeria-orvano', 'Aromatica', 'Salvia Montana',   'salvia-montana',   'hombre', 105000),
    ('023', 'perfumeria-orvano', 'Floral',    'Jazmin Nocturno',  'jazmin-nocturno',  'mujer',  115000),
    ('024', 'perfumeria-orvano', 'Amaderada', 'Vetiver Gris',     'vetiver-gris',     'hombre', 120000),
    ('025', 'perfumeria-orvano', 'Oriental',  'Ambar Oscuro',     'ambar-oscuro',     'hombre', 130000),
    ('026', 'aromas-lumbre',     'Aromatica', 'Brisa de Menta',   'brisa-de-menta',   'unisex',  80000),
    ('027', 'aromas-lumbre',     'Acuatica',  'Gota de Rocio',    'gota-de-rocio',    'mujer',   85000),
    ('028', 'aromas-lumbre',     'Floral',    'Azahar Dulce',     'azahar-dulce',     'mujer',   95000),
    ('029', 'aromas-lumbre',     'Amaderada', 'Bosque Hondo',     'bosque-hondo',     'unisex', 100000),
    ('030', 'aromas-lumbre',     'Oriental',  'Cacao Suave',      'cacao-suave',      'unisex', 110000)
) AS v(codigo, marca_slug, familia, nombre, slug, genero, precio_30);

-- =====================================================
-- Productos
-- =====================================================
INSERT INTO productos (marca_id, familia_olfativa_id, nombre, slug, descripcion, genero)
SELECT m.id, f.id, c.nombre, c.slug,
       CASE c.familia
           WHEN 'Citrica'   THEN 'Fragancia citrica, fresca y luminosa para el dia.'
           WHEN 'Floral'    THEN 'Fragancia floral, delicada y elegante.'
           WHEN 'Amaderada' THEN 'Fragancia amaderada, calida y envolvente.'
           WHEN 'Oriental'  THEN 'Fragancia oriental, intensa y persistente.'
           WHEN 'Acuatica'  THEN 'Fragancia acuatica, limpia y refrescante.'
           WHEN 'Aromatica' THEN 'Fragancia aromatica con notas de hierbas.'
       END,
       c.genero
FROM tmp_catalogo c
JOIN marcas m             ON m.slug = c.marca_slug
JOIN familias_olfativas f ON f.nombre = c.familia
ON CONFLICT DO NOTHING;

-- =====================================================
-- Presentaciones: 30, 50 y 100 ml por producto (precios de referencia en COP)
-- =====================================================
INSERT INTO presentaciones (producto_id, sku, tamano_ml, precio_cop)
SELECT p.id,
       'PP-' || c.codigo || '-' || t.ml,
       t.ml,
       CASE t.ml
           WHEN 30  THEN c.precio_30
           WHEN 50  THEN round(c.precio_30 * 1.6, -3)
           ELSE          round(c.precio_30 * 2.7, -3)
       END
FROM tmp_catalogo c
JOIN productos p ON p.slug = c.slug
CROSS JOIN (VALUES (30), (50), (100)) AS t(ml)
ON CONFLICT DO NOTHING;

DROP TABLE tmp_catalogo;