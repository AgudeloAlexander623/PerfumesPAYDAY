-- =====================================================
-- catalog_db: marcas, familias olfativas, productos y presentaciones
-- =====================================================
\connect catalog_db

CREATE TABLE marcas (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre  VARCHAR(100) NOT NULL UNIQUE,
    slug    VARCHAR(120) NOT NULL UNIQUE,
    activa  BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE familias_olfativas (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre  VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE productos (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    marca_id             UUID         NOT NULL REFERENCES marcas(id),
    familia_olfativa_id  UUID         NOT NULL REFERENCES familias_olfativas(id),
    nombre               VARCHAR(150) NOT NULL,
    slug                 VARCHAR(170) NOT NULL UNIQUE,
    descripcion          TEXT,
    genero               VARCHAR(10)  NOT NULL
                         CHECK (genero IN ('hombre', 'mujer', 'unisex')),
    url_imagen           VARCHAR(500),
    activo               BOOLEAN      NOT NULL DEFAULT TRUE,
    creado_en            TIMESTAMPTZ  NOT NULL DEFAULT now(),
    actualizado_en       TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE presentaciones (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    producto_id  UUID          NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    sku          VARCHAR(50)   NOT NULL UNIQUE,
    tamano_ml    INT           NOT NULL CHECK (tamano_ml > 0),
    precio_cop   NUMERIC(12,2) NOT NULL CHECK (precio_cop >= 0),
    activa       BOOLEAN       NOT NULL DEFAULT TRUE,
    UNIQUE (producto_id, tamano_ml)
);

CREATE INDEX idx_productos_marca    ON productos(marca_id);
CREATE INDEX idx_productos_familia  ON productos(familia_olfativa_id);
CREATE INDEX idx_productos_genero   ON productos(genero);
CREATE INDEX idx_presentaciones_producto ON presentaciones(producto_id);