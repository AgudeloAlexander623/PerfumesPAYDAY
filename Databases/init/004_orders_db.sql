-- =====================================================
-- orders_db: direcciones, carritos, pedidos y pagos
-- usuario_id y presentacion_id son referencias logicas
-- (apuntan a otras bases de datos, por eso no tienen FK)
-- =====================================================
\connect orders_db

CREATE TABLE direcciones (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id           UUID         NOT NULL,
    nombre_destinatario  VARCHAR(150) NOT NULL,
    telefono             VARCHAR(20)  NOT NULL,
    departamento         VARCHAR(80)  NOT NULL,
    ciudad               VARCHAR(80)  NOT NULL,
    direccion            VARCHAR(200) NOT NULL,
    referencias          TEXT,
    es_principal         BOOLEAN      NOT NULL DEFAULT FALSE,
    creado_en            TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE carritos (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id      UUID        NOT NULL UNIQUE,
    actualizado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE items_carrito (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    carrito_id       UUID NOT NULL REFERENCES carritos(id) ON DELETE CASCADE,
    presentacion_id  UUID NOT NULL,
    cantidad         INT  NOT NULL CHECK (cantidad > 0),
    UNIQUE (carrito_id, presentacion_id)
);

CREATE TABLE pedidos (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id                UUID          NOT NULL,
    estado                    VARCHAR(20)   NOT NULL DEFAULT 'pagado_simulado'
                              CHECK (estado IN ('pagado_simulado', 'cancelado')),
    total_cop                 NUMERIC(12,2) NOT NULL CHECK (total_cop >= 0),
    envio_nombre_destinatario VARCHAR(150)  NOT NULL,
    envio_telefono            VARCHAR(20)   NOT NULL,
    envio_departamento        VARCHAR(80)   NOT NULL,
    envio_ciudad              VARCHAR(80)   NOT NULL,
    envio_direccion           VARCHAR(200)  NOT NULL,
    envio_referencias         TEXT,
    creado_en                 TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE TABLE items_pedido (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pedido_id            UUID          NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    presentacion_id      UUID          NOT NULL,
    nombre_producto      VARCHAR(150)  NOT NULL,
    nombre_marca         VARCHAR(100)  NOT NULL,
    tamano_ml            INT           NOT NULL,
    precio_unitario_cop  NUMERIC(12,2) NOT NULL CHECK (precio_unitario_cop >= 0),
    cantidad             INT           NOT NULL CHECK (cantidad > 0)
);

CREATE TABLE pagos (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pedido_id  UUID          NOT NULL UNIQUE REFERENCES pedidos(id) ON DELETE CASCADE,
    metodo     VARCHAR(20)   NOT NULL DEFAULT 'simulado',
    estado     VARCHAR(30)   NOT NULL DEFAULT 'aprobado_simulado',
    monto_cop  NUMERIC(12,2) NOT NULL CHECK (monto_cop >= 0),
    creado_en  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE INDEX idx_direcciones_usuario  ON direcciones(usuario_id);
CREATE INDEX idx_pedidos_usuario      ON pedidos(usuario_id);
CREATE INDEX idx_items_pedido_pedido  ON items_pedido(pedido_id);