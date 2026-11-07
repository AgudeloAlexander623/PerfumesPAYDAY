\connect security_db

INSERT INTO roles (nombre) VALUES ('cliente'), ('admin')
ON CONFLICT (nombre) DO NOTHING;