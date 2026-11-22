\connect catalog_db

CREATE TABLE calidades (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo       VARCHAR(20)  NOT NULL UNIQUE,
    nombre       VARCHAR(60)  NOT NULL,
    descripcion  VARCHAR(255)
);

ALTER TABLE productos ADD COLUMN calidad_id UUID REFERENCES calidades(id);

CREATE INDEX idx_productos_calidad ON productos(calidad_id);