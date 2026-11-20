\connect security_db

INSERT INTO roles (nombre) VALUES ('cliente'), ('manager'), ('admin')
ON CONFLICT (nombre) DO NOTHING;