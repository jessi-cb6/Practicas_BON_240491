
/* Eliminar usuarios si ya existen */
DROP USER IF EXISTS 'marco.ramirez'@'%';
DROP USER IF EXISTS 'jessica.cruz'@'%';
DROP USER IF EXISTS 'luis.angel'@'%';
DROP USER IF EXISTS 'manuel.cruz'@'%';
DROP USER IF EXISTS 'julieta.barona'@'%';

/* Creación de usuarios remotos */
CREATE USER 'marco.ramirez'@'%' IDENTIFIED BY 'qwerty123';
CREATE USER 'jessica.cruz'@'%' IDENTIFIED BY '240491';
CREATE USER 'luis.angel'@'%' IDENTIFIED BY '240492';
CREATE USER 'manuel.cruz'@'%' IDENTIFIED BY '240490';
CREATE USER 'julieta.barona'@'%' IDENTIFIED BY '240493';

/*usuarios middleware*/
CREATE USER IF NOT EXISTS 'app_web' IDENTIFIED BY 'web123'
CREATE USER IF NOT EXISTS 'app_mobile' IDENTIFIED BY 'mobile123'


/* Asignar privilegios solo a Jessica */
GRANT ALL PRIVILEGES ON *.* TO 'jessica.cruz'@'%';

/* Privilegios de consulta, inserción, actualización y eliminación */
GRANT SELECT, INSERT, UPDATE, DELETE
ON db_test_7b.*
TO 'luis.angel'@'%';

/* Creación de roles para el sistema de ecommerce */
CREATE ROLE IF NOT EXISTS 'superadmin';
CREATE ROLE IF NOT EXISTS 'admin';
CREATE ROLE IF NOT EXISTS 'seller';
CREATE ROLE IF NOT EXISTS 'buyer';
CREATE ROLE IF NOT EXISTS 'support';
CREATE ROLE IF NOT EXISTS 'common';
CREATE ROLE IF NOT EXISTS 'user_not_registered';

/* Asignar privilegios a los roles */
GRANT ALL PRIVILEGES ON db_test_7b.* TO 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'superadmin';

/* Privilegios del rol support */
GRANT SELECT, INSERT, UPDATE ON db_test_7b.tb_users TO 'support';
GRANT SELECT, INSERT, UPDATE ON db_test_7b.tb_products TO 'support';
GRANT SELECT, INSERT, UPDATE ON db_test_7b.tbc_categories TO 'support';
GRANT SELECT, INSERT, UPDATE ON db_test_7b.tbd_products_categories TO 'support';

/* Privilegios del rol seller */
GRANT SELECT, INSERT, UPDATE ON db_test_7b.tb_products TO 'seller';

/* Privilegios para usuarios no registrados */
GRANT INSERT ON db_test_7b.tb_users TO 'user_not_registered';
GRANT INSERT ON db_test_7b.tb_people TO 'user_not_registered';

GRANT EXECUTE  ON PROCEDURE db_test_7b.sp_register_new_user TO 'user_not_registered';


/* Asignar roles a los usuarios */
GRANT 'admin' TO 'marco.ramirez'@'%';
GRANT 'superadmin' TO 'jessica.cruz'@'%';
GRANT 'seller' TO 'luis.angel'@'%';
GRANT 'seller' TO 'manuel.cruz'@'%';
GRANT 'support' TO 'julieta.barona'@'%';

/*asignar roles a las credenciales de conexion de las apps*/
GRANT 'user_not_registered' to  'app_web'@'%';
GRANT 'user_not_registered' to  'app_mobile'@'%';


/* Configurar roles predeterminados */
SET DEFAULT ROLE 'admin' TO 'marco.ramirez'@'%';
SET DEFAULT ROLE 'seller' TO 'manuel.cruz'@'%';
SET DEFAULT ROLE 'support' TO 'julieta.barona'@'%';

SET DEFAULT ROLE 'user_not_registered' TO 'app_web'@'%';
SET DEFAULT ROLE 'user_not_registered' TO 'app_mobile'@'%';

