\connect catalog_db

CREATE TABLE inventario (
    presentacion_id  UUID PRIMARY KEY REFERENCES presentaciones(id) ON DELETE CASCADE,
    cantidad         INT         NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    actualizado_en   TIMESTAMPTZ NOT NULL DEFAULT now()
);