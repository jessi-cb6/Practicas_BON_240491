/*Elimoinar usuarios si ya existen */
DROP USER IF EXISTS 'marco.ramirez'@'%';
DROP USER IF EXISTS 'jessica.cruz'@'%';
DROP USER IF EXISTS 'luis.angel'@'%';
DROP USER IF EXISTS 'manuel.cruz'@'%';
DROP USER IF EXISTS 'julieta.barona'@'%';


/* creacion d usuarios remotos*/
CREATE USER 'marco.ramirez'@'%' IDENTIFIED BY 'qwerty123';
CREATE USER 'jessica.cruz'@'%' IDENTIFIED BY '240491';
CREATE USER 'luis.angel'@'%' IDENTIFIED BY '240492';
CREATE USER 'manuel.cruz'@'%' IDENTIFIED BY '240490';
CREATE USER 'julieta.barona'@'%' IDENTIFIED BY '240493';


/*Asignar los privilegios s0lo yop*/
GRANT ALL PRIVILEGES ON *.* TO 'jessica.cruz'@'%';
/*Asignar privilegios de seleccion,inserccion,actualizacion y eliminacion al usuario de la izquierda*/
GRANT SELECT, INSERT, UPDATE, DELETE ON  db_test.* TO 'luis.angel'@'%';

/*creacion de roles para el sistema de ecomerce*/
CREATE ROLE IF NOT EXISTS 'superadmin';
CREATE ROLE IF NOT EXISTS 'admin';
CREATE ROLE IF NOT EXISTS  'seller';
CREATE ROLE IF NOT EXISTS 'buyer';
CREATE ROLE IF NOT EXISTS 'support';
CREATE ROLE IF NOT EXISTS 'common';
CREATE ROLE IF NOT EXISTS 'user_not_registered';

/*Asignar privilegios a los roles creados*/
GRANT ALL PRIVILEGES ON db_test.* TO 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'superadmin';

GRANT SELECT, INSERT, UPDATE ON db_test.tb_users TO 'support'; 
GRANT SELECT, INSERT, UPDATE ON db_test.tb_products TO 'support';

GRANT SELECT, INSERT, UPDATE ON db_test.tb_products TO 'seller';


 
 /*asignar roles a los usuarios creados*/
GRANT 'admin' TO 'marco.ramirez'@'%';
GRANT 'superadmin' TO 'jessica.cruz'@'%';
GRANT 'seller' TO 'luis.angel'@'%';
GRANT 'seller' TO 'manuel.cruz'@'%';
GRANT 'support' TO 'julieta.barona'@'%';


set default role 'admin'
to 'marco.ramirez'@'%';
set default role 'seller'
to 'manuel.cruz'@'%';
set default role 'support'
to 'julieta.barona'@'%';
