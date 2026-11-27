\connect security_db

-- Catalogo de permisos
INSERT INTO permisos (codigo, descripcion) VALUES
    ('panel_local.acceder',       'Acceder a los paneles de la perfumeria'),
    ('catalogo.gestionar',        'Crear y editar marcas, productos y presentaciones'),
    ('pedidos.consultar',         'Consultar los pedidos'),
    ('pedidos.gestionar',         'Gestionar el estado de los pedidos'),
    ('usuarios.gestionar',        'Administrar usuarios y roles'),
    ('seguridad.acceder',         'Acceder al panel de seguridad'),
    ('configuracion.gestionar',   'Modificar la configuracion del sistema'),
    ('auditoria.consultar',       'Consultar los registros de auditoria'),
    ('datos_sensibles.consultar', 'Ver informacion sensible')
ON CONFLICT (codigo) DO NOTHING;

-- Manager: solo gestion del local
INSERT INTO rol_permisos (rol_id, permiso_id)
SELECT r.id, p.id
FROM roles r
JOIN permisos p ON p.codigo IN (
    'panel_local.acceder', 'catalogo.gestionar',
    'pedidos.consultar', 'pedidos.gestionar'
)
WHERE r.nombre = 'manager'
ON CONFLICT DO NOTHING;

-- Admin: todos los permisos
INSERT INTO rol_permisos (rol_id, permiso_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permisos p
WHERE r.nombre = 'admin'
ON CONFLICT DO NOTHING;