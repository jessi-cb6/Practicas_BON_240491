-- ============================================================================
-- SCRIPT OPTIMIZADO DE POSTGRESQL 15/16/17: DDL, ROLES, TRIGGERS, ÍNDICES Y VISTAS
-- Base de Datos: db_test_7b
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. ESTRUCTURA DE TABLAS (DDL)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS tb_logs CASCADE;
DROP TABLE IF EXISTS tb_products CASCADE;
DROP TABLE IF EXISTS tb_users CASCADE;

CREATE TABLE tb_users (
    ID SERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    nick VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tb_products (
    ID SERIAL PRIMARY KEY,
    SKU VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    current_price DECIMAL(10,2) NOT NULL,
    current_stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tb_logs (
    ID SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    table_operation VARCHAR(10) NOT NULL,
    record_id INT NOT NULL,
    db_user VARCHAR(100) NOT NULL,
    operation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation_description TEXT NOT NULL,
    operation_status BOOLEAN NOT NULL DEFAULT TRUE
);

-- ----------------------------------------------------------------------------
-- 2. ÍNDICE DE OPTIMIZACIÓN (Fórmula de alto rendimiento para Auditoría)
-- ----------------------------------------------------------------------------
CREATE INDEX idx_logs_trazabilidad 
ON tb_logs (table_name, record_id, operation_date DESC);

-- ----------------------------------------------------------------------------
-- 3. ROLES DEL SISTEMA Y USUARIOS
-- ----------------------------------------------------------------------------
DROP ROLE IF EXISTS superadmin, admin, seller, buyer, guest, support, common, user_not_registered;

-- Creación de Roles
CREATE ROLE superadmin WITH SUPERUSER CREATEDB CREATEROLE; -- Control total del servidor PostgreSQL
CREATE ROLE admin;                                         -- Administrador de la BD
CREATE ROLE seller;
CREATE ROLE buyer;
CREATE ROLE guest;
CREATE ROLE support;
CREATE ROLE common;
CREATE ROLE user_not_registered;

-- Asignación de Privilegios a Roles sobre el Esquema y Tablas
GRANT ALL PRIVILEGES ON DATABASE db_test_7b TO admin;
GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

GRANT SELECT, INSERT, UPDATE ON tb_users TO support;
GRANT SELECT, INSERT, UPDATE ON tb_products TO support;
GRANT SELECT, INSERT, UPDATE ON tb_products TO seller;
GRANT SELECT ON tb_products TO buyer, guest, common;

-- Indispensable para los INSERTs de ID autoincrementables (SERIAL)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO support, seller;

-- Privilegios automáticos para objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin;

-- Creación de Cuentas de Usuario
DROP USER IF EXISTS "angel.hernandez";
DROP USER IF EXISTS "luis.hernandez";
DROP USER IF EXISTS "marco.ramirez";
DROP USER IF EXISTS "jhonatan.ibarra";
DROP USER IF EXISTS "jessica.cruz";
DROP USER IF EXISTS "dorian.barrios";

CREATE USER "angel.hernandez" WITH PASSWORD '240490';
CREATE USER "luis.hernandez" WITH PASSWORD '240492';
CREATE USER "marco.ramirez" WITH PASSWORD 'qwerty123';
CREATE USER "jhonatan.ibarra" WITH PASSWORD '240080!';
CREATE USER "jessica.cruz" WITH PASSWORD '240491';
CREATE USER "dorian.barrios" WITH PASSWORD '240065';

-- Permisos directos al usuario sin rol (dorian.barrios)
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "dorian.barrios";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO "dorian.barrios";

-- Asignación de Roles a Cuentas
GRANT superadmin TO "jessica.cruz";
GRANT admin TO "marco.ramirez";
GRANT seller TO "jhonatan.ibarra";
GRANT seller TO "luis.hernandez";
GRANT support TO "angel.hernandez";

-- ----------------------------------------------------------------------------
-- 4. TRIGGERS DE AUDITORÍA (tb_users)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_trg_users_audit()
RETURNS TRIGGER AS $$
DECLARE
    v_record_id INT;
    v_desc TEXT;
    v_op VARCHAR(10);
BEGIN
    IF (TG_OP = 'INSERT') THEN
        v_op := 'Create';
        v_record_id := NEW.ID;
        v_desc := CONCAT('Usuario creado ID: ', NEW.ID, ', Email: ', NEW.email, ', Nick: ', NEW.nick);
        
    ELSIF (TG_OP = 'UPDATE') THEN
        v_op := 'Update';
        v_record_id := NEW.ID;
        v_desc := CONCAT('Usuario actualizado ID: ', NEW.ID, ', Email anterior: ', OLD.email, ', Email nuevo: ', NEW.email);
        
    ELSIF (TG_OP = 'DELETE') THEN
        v_op := 'Delete';
        v_record_id := OLD.ID;
        v_desc := CONCAT('Usuario eliminado ID: ', OLD.ID, ', Email: ', OLD.email);
    END IF;

    INSERT INTO tb_logs (
        table_name,
        table_operation,
        record_id,
        db_user,
        operation_date,
        operation_description,
        operation_status
    )
    VALUES (
        'tb_users',
        v_op,
        v_record_id,
        CURRENT_USER,
        CURRENT_TIMESTAMP,
        v_desc,
        TRUE
    );

    IF (TG_OP = 'DELETE') THEN
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_users_audit ON tb_users;
CREATE TRIGGER trg_users_audit
AFTER INSERT OR UPDATE OR DELETE ON tb_users
FOR EACH ROW EXECUTE FUNCTION fn_trg_users_audit();

-- ----------------------------------------------------------------------------
-- 5. TRIGGERS DE AUDITORÍA (tb_products)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_trg_products_audit()
RETURNS TRIGGER AS $$
DECLARE
    v_record_id INT;
    v_desc TEXT;
    v_op VARCHAR(10);
BEGIN
    IF (TG_OP = 'INSERT') THEN
        v_op := 'Create';
        v_record_id := NEW.ID;
        v_desc := CONCAT('Producto creado SKU: ', NEW.SKU, ', Nombre: ', NEW.name, ', Precio: ', NEW.current_price);
        
    ELSIF (TG_OP = 'UPDATE') THEN
        v_op := 'Update';
        v_record_id := NEW.ID;
        v_desc := CONCAT('Producto actualizado SKU: ', NEW.SKU, ', Precio anterior: ', OLD.current_price, ', Precio nuevo: ', NEW.current_price);
        
    ELSIF (TG_OP = 'DELETE') THEN
        v_op := 'Delete';
        v_record_id := OLD.ID;
        v_desc := CONCAT('Producto eliminado SKU: ', OLD.SKU, ', Nombre: ', OLD.name);
    END IF;

    INSERT INTO tb_logs (
        table_name,
        table_operation,
        record_id,
        db_user,
        operation_date,
        operation_description,
        operation_status
    )
    VALUES (
        'tb_products',
        v_op,
        v_record_id,
        CURRENT_USER,
        CURRENT_TIMESTAMP,
        v_desc,
        TRUE
    );

    IF (TG_OP = 'DELETE') THEN
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_products_audit ON tb_products;
CREATE TRIGGER trg_products_audit
AFTER INSERT OR UPDATE OR DELETE ON tb_products
FOR EACH ROW EXECUTE FUNCTION fn_trg_products_audit();

-- ----------------------------------------------------------------------------
-- 6. VISTAS DE TRAZABILIDAD
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_trazabilidad_usuarios AS
SELECT 
    l.ID AS log_id,
    l.table_operation AS accion,
    l.record_id AS usuario_afectado_id,
    l.db_user AS ejecutado_por,
    l.operation_date AS fecha_hora,
    l.operation_description AS detalle
FROM tb_logs l
WHERE l.table_name = 'tb_users'
ORDER BY l.operation_date DESC;

CREATE OR REPLACE VIEW vw_trazabilidad_productos AS
SELECT 
    l.ID AS log_id,
    l.table_operation AS accion,
    l.record_id AS producto_afectado_id,
    l.db_user AS ejecutado_por,
    l.operation_date AS fecha_hora,
    l.operation_description AS detalle
FROM tb_logs l
WHERE l.table_name = 'tb_products'
ORDER BY l.operation_date DESC;