-- =====================================================
-- security_db: usuarios, roles, tokens y auditoria
-- =====================================================
\connect security_db;

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    correo VARCHAR(255) UNIQUE NOT NULL UNIQUE,
    hash_contraseña VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE roles (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre  VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuario_roles (
    usuario_id  UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    rol_id      UUID NOT NULL REFERENCES roles(id)    ON DELETE CASCADE,
    PRIMARY KEY (usuario_id, rol_id)
);

CREATE TABLE tokens_refresco (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    hash_token VARCHAR(255) NOT NULL UNIQUE,
    expira_en TIMESTAMPTZ NOT NULL,
    revocado_en TIMESTAMPTZ,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE registros_auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_usuario_id UUID NOT NULL REFERENCES usuarios(id),
    accion VARCHAR(100) NOT NULL,
    tipo_entidad VARCHAR(100) NOT NULL,
    entidad_id UUID,
    detalles JSONB,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

---- Indices en las llaves foraneas (aceleran los JOIN y las consultas por usuario)
CREATE INDEX idx_tokens_refresco_usuario ON tokens_refresco(usuario_id);
CREATE INDEX idx_auditoria_admin         ON registros_auditoria(admin_usuario_id);