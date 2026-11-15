\connect security_db

CREATE TABLE permisos (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo       VARCHAR(80)  NOT NULL UNIQUE,
    descripcion  VARCHAR(200) NOT NULL
);

CREATE TABLE rol_permisos (
    rol_id      UUID NOT NULL REFERENCES roles(id)    ON DELETE CASCADE,
    permiso_id  UUID NOT NULL REFERENCES permisos(id) ON DELETE CASCADE,
    PRIMARY KEY (rol_id, permiso_id)
);

ALTER TABLE registros_auditoria RENAME COLUMN admin_usuario_id TO usuario_id;
ALTER INDEX idx_auditoria_admin RENAME TO idx_auditoria_usuario;