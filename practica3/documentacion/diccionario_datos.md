# Diccionario de datos — db_test_7b

**Fuente SQL:** `respaldos/db_test_jessi.sql` (3,546,495 bytes).  
**Motor:** MySQL 8.0.36, según la cabecera del respaldo.  
**Alcance:** definiciones y filas incluidas en el archivo; las cantidades no representan el servidor actual.

## Resumen

El respaldo contiene 15 tablas físicas, 113 columnas, 20,252 filas en 16 sentencias INSERT, 20 claves foráneas declaradas, 5 vistas, 2 procedimientos y 39 triggers.

| Tabla | Columnas | Filas del respaldo | Descripción |
|---|---:|---:|---|
| `tb_buyer_orders` | 8 | 0 | Cabecera de pedidos recibidos por un vendedor. Registra importes de subtotal y envío, etapa de cumplimiento, vigencia y fechas; las restricciones CHECK requieren importes no negativos. |
| `tb_carts` | 5 | 0 | Carrito de compra vinculado a una cuenta. La clave UNIQUE de user_ID limita a un carrito por usuario. |
| `tb_logs` | 8 | 10,136 | Bitácora de auditoría que almacena la entidad y operación afectadas, actor, fecha, descripción y resultado. product_id es una referencia informativa opcional, no una FK declarada. |
| `tb_products` | 9 | 5,007 | Catálogo de productos con SKU único, descripción, precio actual, existencias, estado y marcas temporales. |
| `tb_user_addresses` | 12 | 0 | Direcciones de entrega de las cuentas, con etiqueta, destinatario, instrucciones, coordenadas opcionales y marcas de vigencia. CHECK valida rangos y presencia conjunta de coordenadas. |
| `tb_users` | 8 | 11 | Cuentas de usuario con correo y alias únicos, credencial, estado y fechas de alta, actualización y último acceso. |
| `tbc_categories` | 7 | 100 | Catálogo jerárquico de categorías. Cada categoría puede referir opcionalmente a una categoría superior de la misma tabla. |
| `tbc_payment_methods_types` | 6 | 0 | Catálogo de tipos de método de pago con código único, descripción, estado y fechas de mantenimiento. |
| `tbd_address_components` | 8 | 0 | Componentes que desglosan una dirección. Una FK vincula con la dirección y otra, compuesta, enlaza opcionalmente el componente padre dentro de la misma dirección. |
| `tbd_carts_items` | 5 | 0 | Líneas de carrito identificadas por carrito, proveedor y producto. quantity debe ser mayor que cero. |
| `tbd_order_items` | 9 | 0 | Líneas históricas de pedido con producto/proveedor, nombre copiado, cantidad y precio unitario. subtotal es una columna generada almacenada como cantidad por precio. |
| `tbd_products_categories` | 5 | 4,998 | Tabla puente entre productos y categorías. Su clave primaria compuesta impide duplicar una pareja producto-categoría. |
| `tbd_products_users_providers` | 7 | 0 | Tabla puente que registra la relación de un usuario con un producto como titular, revendedor o distribuidor, junto con disponibilidad y estado. |
| `tbd_user_payment_methods` | 11 | 0 | Métodos de pago asociados a usuarios y a un tipo del catálogo. El par proveedor/referencia externa es único. |
| `tbd_users_wishlist_products` | 5 | 0 | Tabla puente de productos guardados por usuarios en listas de deseos, con estado y fechas. |

## Diccionario detallado

### tb_buyer_orders

**Descripción.** Cabecera de pedidos recibidos por un vendedor. Registra importes de subtotal y envío, etapa de cumplimiento, vigencia y fechas; las restricciones CHECK requieren importes no negativos.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `seller_ID` | `int` | Entero INT de 32 bits con signo. | Usuario vendedor asociado al pedido; FK a tb_users.ID. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tb_users`.`ID` |
| `subtotal` | `decimal(12,2)` | Decimal exacto DECIMAL(12,2): hasta 10 dígitos enteros y 2 decimales. | Importe subtotal del pedido; CHECK requiere valor no negativo. | Cuantitativa continua; importe | NOT NULL; DEFAULT '0.00' | — |
| `shipping_cost` | `decimal(12,2)` | Decimal exacto DECIMAL(12,2): hasta 10 dígitos enteros y 2 decimales. | Importe del envío; CHECK requiere valor no negativo. | Cuantitativa continua; importe | NOT NULL; DEFAULT '0.00' | — |
| `fulfillment_status` | `enum('Pending','Accepted','Preparing','Sent','Delivered','Canceled','Returned')` | Valores textuales cerrados: Pending, Accepted, Preparing, Sent, Delivered, Canceled, Returned. | Estado de cumplimiento del pedido, limitado a Pending, Accepted, Preparing, Sent, Delivered, Canceled o Returned. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT 'Pending' | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `KEY `seller_ID` (`seller_ID`)`
- `CONSTRAINT `tb_buyer_orders_ibfk_1` FOREIGN KEY (`seller_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `tb_buyer_orders_chk_1` CHECK ((`subtotal` >= 0))`
- `CONSTRAINT `tb_buyer_orders_chk_2` CHECK ((`shipping_cost` >= 0))`

### tb_carts

**Descripción.** Carrito de compra vinculado a una cuenta. La clave UNIQUE de user_ID limita a un carrito por usuario.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `user_ID` | `int` | Entero INT de 32 bits con signo. | Identificador de usuario; según la tabla es FK, parte de PK o clave UNIQUE. | Cualitativa nominal; identificador/código | UNIQUE; FK; NOT NULL | `tb_users`.`ID` |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_cart_user` (`user_ID`)`
- `CONSTRAINT `tb_carts_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### tb_logs

**Descripción.** Bitácora de auditoría que almacena la entidad y operación afectadas, actor, fecha, descripción y resultado. product_id es una referencia informativa opcional, no una FK declarada.

**Filas incluidas en SQL:** 10,136.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int` | Entero INT de 32 bits con signo. | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `table_name` | `varchar(80)` | Cadena de longitud variable, máximo 80 caracteres; no se declara otro patrón. | Nombre textual de la tabla/entidad registrada en la bitácora. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `table_operation` | `enum('Create','Read','Update','Delete')` | Valores textuales cerrados: Create, Read, Update, Delete. | Operación auditada, limitada al ENUM declarado. | Cualitativa nominal; categoría/indicador | NULL; DEFAULT NULL | — |
| `db_user` | `varchar(80)` | Cadena de longitud variable, máximo 80 caracteres; no se declara otro patrón. | Actor de base de datos consignado en el evento. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `operation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora en que se registró la operación. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `operation_description` | `text` | Texto de longitud variable; el DDL no fija un límite funcional menor. | Detalle textual del evento auditado. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `operation_status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de resultado; el DDL no define qué valor representa éxito o error. | Cualitativa nominal; categoría/indicador | NULL; DEFAULT b'1' | — |
| `product_id` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador opcional relacionado con el evento; no tiene FOREIGN KEY declarada. | Cualitativa nominal; identificador/código | NULL; DEFAULT NULL | Posible `tb_products`.`ID` por nombre/uso; no declarada como FK. |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_logs_table_op_date` (`table_name`,`table_operation`,`operation_date`)`
- `KEY `idx_logs_product_trace` (`table_name`,`table_operation`,`product_id`)`
- `KEY `idx_logs_tabla_operacion` (`table_name`,`table_operation`)`

### tb_products

**Descripción.** Catálogo de productos con SKU único, descripción, precio actual, existencias, estado y marcas temporales.

**Filas incluidas en SQL:** 5,007.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `SKU` | `varchar(50)` | Cadena de longitud variable, máximo 50 caracteres; no se declara otro patrón. | Código comercial único del producto. | Cualitativa nominal; identificador/código | UNIQUE; NOT NULL | — |
| `name` | `varchar(250)` | Cadena de longitud variable, máximo 250 caracteres; no se declara otro patrón. | Nombre legible del producto o categoría. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `description` | `text` | Texto de longitud variable; el DDL no fija un límite funcional menor. | Descripción textual complementaria; no se impone formato en el DDL. | Cualitativa nominal; texto descriptivo | NULL | — |
| `current_price` | `decimal(10,2)` | Decimal exacto DECIMAL(10,2): hasta 8 dígitos enteros y 2 decimales. | Precio monetario vigente del producto. | Cuantitativa continua; importe | NOT NULL; DEFAULT '0.00' | — |
| `current_stock` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Unidades registradas en existencia. | Cuantitativa discreta; conteo/valor entero | NOT NULL; DEFAULT '0' | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `SKU` (`SKU`)`

### tb_user_addresses

**Descripción.** Direcciones de entrega de las cuentas, con etiqueta, destinatario, instrucciones, coordenadas opcionales y marcas de vigencia. CHECK valida rangos y presencia conjunta de coordenadas.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | Entero BIGINT de 64 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `user_ID` | `int` | Entero INT de 32 bits con signo. | Identificador de usuario; según la tabla es FK, parte de PK o clave UNIQUE. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tb_users`.`ID` |
| `address_label` | `varchar(100)` | Cadena de longitud variable, máximo 100 caracteres; no se declara otro patrón. | Etiqueta libre para distinguir la dirección, por ejemplo casa o trabajo. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `recipient_name` | `varchar(150)` | Cadena de longitud variable, máximo 150 caracteres; no se declara otro patrón. | Nombre de quien recibirá el envío; opcional. | Cualitativa nominal; texto descriptivo | NULL; DEFAULT NULL | — |
| `recipient_phone` | `varchar(25)` | Cadena de longitud variable, máximo 25 caracteres; no se declara otro patrón. | Teléfono de contacto opcional, guardado como texto para conservar prefijos y formato. | Cualitativa nominal; texto descriptivo | NULL; DEFAULT NULL | — |
| `delivery_instructions` | `varchar(500)` | Cadena de longitud variable, máximo 500 caracteres; no se declara otro patrón. | Instrucciones opcionales para la entrega. | Cualitativa nominal; texto descriptivo | NULL; DEFAULT NULL | — |
| `latitude` | `decimal(10,7)` | Decimal exacto DECIMAL(10,7): hasta 3 dígitos enteros y 7 decimales. | Latitud decimal opcional; CHECK limita el rango a −90..90 y requiere que ambas coordenadas estén presentes o ausentes. | Cuantitativa continua; coordenada | NULL; DEFAULT NULL | — |
| `longitude` | `decimal(10,7)` | Decimal exacto DECIMAL(10,7): hasta 3 dígitos enteros y 7 decimales. | Longitud decimal opcional; CHECK limita el rango a −180..180 y requiere que ambas coordenadas estén presentes o ausentes. | Cuantitativa continua; coordenada | NULL; DEFAULT NULL | — |
| `is_default` | `tinyint(1)` | Entero de 8 bits declarado tinyint(1); no es un booleano estricto. | Indicador numérico 0/1 de dirección o método predeterminado; tinyint(1) no constituye por sí solo una restricción booleana. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT '0' | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_user_addresses` (`user_ID`)`
- `CONSTRAINT `fk_addresses_users` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `chk_coordinates` CHECK ((((`latitude` is null) and (`longitude` is null)) or ((`latitude` is not null) and (`longitude` is not null))))`
- `CONSTRAINT `chk_latitude` CHECK ((`latitude` between -(90) and 90))`
- `CONSTRAINT `chk_longitude` CHECK ((`longitude` between -(180) and 180))`

### tb_users

**Descripción.** Cuentas de usuario con correo y alias únicos, credencial, estado y fechas de alta, actualización y último acceso.

**Filas incluidas en SQL:** 11.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int` | Entero INT de 32 bits con signo. | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `email` | `varchar(100)` | Cadena de longitud variable, máximo 100 caracteres; no se declara otro patrón. | Correo asociado a la cuenta; la clave UNIQUE exige que no se repita. | Cualitativa nominal; identificador/código | UNIQUE; NOT NULL | — |
| `nick` | `varchar(50)` | Cadena de longitud variable, máximo 50 caracteres; no se declara otro patrón. | Alias de la cuenta; la clave UNIQUE exige que no se repita. | Cualitativa nominal; identificador/código | UNIQUE; NOT NULL | — |
| `password` | `varchar(255)` | Cadena de longitud variable, máximo 255 caracteres; no se declara otro patrón. | Cadena de credencial. El DDL no indica si el contenido está cifrado o resumido; se omite en ejemplos. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL | — |
| `last_login` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora del último acceso; NULL indica que no hay valor almacenado. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NULL; DEFAULT b'1' | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `email` (`email`)`
- `UNIQUE KEY `nick` (`nick`)`

### tbc_categories

**Descripción.** Catálogo jerárquico de categorías. Cada categoría puede referir opcionalmente a una categoría superior de la misma tabla.

**Filas incluidas en SQL:** 100.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `name` | `varchar(120)` | Cadena de longitud variable, máximo 120 caracteres; no se declara otro patrón. | Nombre legible del producto o categoría. | Cualitativa nominal; texto descriptivo | UNIQUE; NOT NULL | — |
| `description` | `text` | Texto de longitud variable; el DDL no fija un límite funcional menor. | Descripción textual complementaria; no se impone formato en el DDL. | Cualitativa nominal; texto descriptivo | NULL | — |
| `sup_id_category` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Categoría superior opcional; FK autorreferente a tbc_categories.ID. | Cualitativa nominal; identificador/código | FK; NULL; DEFAULT NULL | `tbc_categories`.`ID` |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NOT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `name` (`name`)`
- `KEY `fk_superior_category` (`sup_id_category`)`
- `CONSTRAINT `fk_superior_category` FOREIGN KEY (`sup_id_category`) REFERENCES `tbc_categories` (`ID`)`

### tbc_payment_methods_types

**Descripción.** Catálogo de tipos de método de pago con código único, descripción, estado y fechas de mantenimiento.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int` | Entero INT de 32 bits con signo. | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `code` | `varchar(30)` | Cadena de longitud variable, máximo 30 caracteres; no se declara otro patrón. | Código textual único del tipo de método de pago. | Cualitativa nominal; identificador/código | UNIQUE; NOT NULL | — |
| `description` | `text` | Texto de longitud variable; el DDL no fija un límite funcional menor. | Descripción textual complementaria; no se impone formato en el DDL. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `code` (`code`)`

### tbd_address_components

**Descripción.** Componentes que desglosan una dirección. Una FK vincula con la dirección y otra, compuesta, enlaza opcionalmente el componente padre dentro de la misma dirección.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | Entero BIGINT de 64 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; UNIQUE; NOT NULL; AUTO_INCREMENT | — |
| `address_ID` | `bigint unsigned` | Entero BIGINT de 64 bits sin signo (UNSIGNED). | Dirección a la que pertenece el componente; participa en FK a tb_user_addresses y en referencia compuesta al padre. | Cualitativa nominal; identificador/código | UNIQUE; FK; NOT NULL | `tb_user_addresses`.`ID` |
| `value` | `varchar(255)` | Cadena de longitud variable, máximo 255 caracteres; no se declara otro patrón. | Valor textual del componente de dirección. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `component_type` | `varchar(50)` | Cadena de longitud variable, máximo 50 caracteres; no se declara otro patrón. | Tipo textual de componente; no hay catálogo ENUM en el DDL. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `address_sup_ID` | `bigint unsigned` | Entero BIGINT de 64 bits sin signo (UNSIGNED). | Componente padre opcional dentro de la misma dirección; participa en FK compuesta a tbd_address_components(address_ID, ID). | Cualitativa nominal; identificador/código | FK; NULL; DEFAULT NULL | `tbd_address_components`.`address_ID`; `tbd_address_components`.`ID` |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_address_component` (`address_ID`,`ID`)`
- `KEY `idx_address_parent` (`address_ID`,`address_sup_ID`)`
- `CONSTRAINT `fk_component_address` FOREIGN KEY (`address_ID`) REFERENCES `tb_user_addresses` (`ID`) ON DELETE RESTRICT`
- `CONSTRAINT `fk_component_parent` FOREIGN KEY (`address_ID`, `address_sup_ID`) REFERENCES `tbd_address_components` (`address_ID`, `ID`) ON DELETE RESTRICT`

### tbd_carts_items

**Descripción.** Líneas de carrito identificadas por carrito, proveedor y producto. quantity debe ser mayor que cero.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `cart_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Carrito de la línea; FK a tb_carts.ID y parte de la clave primaria compuesta. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tb_carts`.`ID` |
| `provider_ID` | `int` | Entero INT de 32 bits con signo. | Usuario proveedor del producto; participa en la FK compuesta de producto-proveedor. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tbd_products_users_providers`.`user_ID` |
| `product_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador del producto; puede ser FK, parte de PK compuesta o ambas según la tabla. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tbd_products_users_providers`.`product_ID` |
| `quantity` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Cantidad entera de unidades; CHECK requiere un valor mayor que cero. | Cuantitativa discreta; conteo/valor entero | NOT NULL; DEFAULT '1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`cart_ID`,`provider_ID`,`product_ID`)`
- `KEY `provider_ID` (`provider_ID`)`
- `KEY `product_ID` (`product_ID`)`
- `CONSTRAINT `tbd_carts_items_ibfk_1` FOREIGN KEY (`cart_ID`) REFERENCES `tb_carts` (`ID`)`
- `CONSTRAINT `tbd_carts_items_ibfk_2` FOREIGN KEY (`provider_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`)`
- `CONSTRAINT `tbd_carts_items_ibfk_3` FOREIGN KEY (`product_ID`) REFERENCES `tbd_products_users_providers` (`product_ID`)`
- `CONSTRAINT `chk_cart_quantity` CHECK ((`quantity` > 0))`

### tbd_order_items

**Descripción.** Líneas históricas de pedido con producto/proveedor, nombre copiado, cantidad y precio unitario. subtotal es una columna generada almacenada como cantidad por precio.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `seller_order_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Pedido al que pertenece la línea; FK a tb_buyer_orders.ID. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tb_buyer_orders`.`ID` |
| `product_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador del producto; puede ser FK, parte de PK compuesta o ambas según la tabla. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tbd_products_users_providers`.`product_ID` |
| `provider_ID` | `int` | Entero INT de 32 bits con signo. | Usuario proveedor del producto; participa en la FK compuesta de producto-proveedor. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tbd_products_users_providers`.`user_ID` |
| `product_name` | `varchar(255)` | Cadena de longitud variable, máximo 255 caracteres; no se declara otro patrón. | Nombre del producto guardado como instantánea en la línea; no es FK. | Cualitativa nominal; texto descriptivo | NOT NULL | — |
| `quantity` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Cantidad entera de unidades; CHECK requiere un valor mayor que cero. | Cuantitativa discreta; conteo/valor entero | NOT NULL | — |
| `unit_price` | `decimal(12,2)` | Decimal exacto DECIMAL(12,2): hasta 10 dígitos enteros y 2 decimales. | Precio unitario monetario de la línea; CHECK exige valor no negativo. | Cuantitativa continua; importe | NOT NULL | — |
| `subtotal` | `decimal(12,2)` | Decimal exacto DECIMAL(12,2): hasta 10 dígitos enteros y 2 decimales. | Importe subtotal del pedido; CHECK requiere valor no negativo. | Cuantitativa continua; importe | NULL; GENERATED ALWAYS AS ((`quantity` * `unit_price`)) STORED | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `KEY `seller_order_ID` (`seller_order_ID`)`
- `KEY `product_ID` (`product_ID`)`
- `KEY `provider_ID` (`provider_ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_1` FOREIGN KEY (`seller_order_ID`) REFERENCES `tb_buyer_orders` (`ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_2` FOREIGN KEY (`product_ID`) REFERENCES `tbd_products_users_providers` (`product_ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_3` FOREIGN KEY (`provider_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`)`
- `CONSTRAINT `tbd_order_items_chk_1` CHECK ((`quantity` > 0))`
- `CONSTRAINT `tbd_order_items_chk_2` CHECK ((`unit_price` >= 0))`

### tbd_products_categories

**Descripción.** Tabla puente entre productos y categorías. Su clave primaria compuesta impide duplicar una pareja producto-categoría.

**Filas incluidas en SQL:** 4,998.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `product_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador del producto; puede ser FK, parte de PK compuesta o ambas según la tabla. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tb_products`.`ID` |
| `categories_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador de categoría; FK y parte de la PK de la tabla puente. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tbc_categories`.`ID` |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`product_ID`,`categories_ID`)`
- `KEY `fk_tbd_pc_category` (`categories_ID`)`
- `KEY `idx_pc_producto_categoria` (`product_ID`,`categories_ID`)`
- `CONSTRAINT `fk_tbd_pc_category` FOREIGN KEY (`categories_ID`) REFERENCES `tbc_categories` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE`
- `CONSTRAINT `fk_tbd_pc_product` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE`

### tbd_products_users_providers

**Descripción.** Tabla puente que registra la relación de un usuario con un producto como titular, revendedor o distribuidor, junto con disponibilidad y estado.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `user_ID` | `int` | Entero INT de 32 bits con signo. | Identificador de usuario; según la tabla es FK, parte de PK o clave UNIQUE. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tb_users`.`ID` |
| `product_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador del producto; puede ser FK, parte de PK compuesta o ambas según la tabla. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tb_products`.`ID` |
| `type_ownership` | `enum('Owner','Reseller','Distributor')` | Valores textuales cerrados: Owner, Reseller, Distributor. | Tipo de relación permitido por ENUM: Owner, Reseller o Distributor. | Cualitativa nominal; categoría/indicador | NULL; DEFAULT NULL | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `available_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora desde la que se declara disponible la relación usuario-producto. | Temporal; fecha y hora (escala no asignada) | NOT NULL | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`user_ID`,`product_ID`)`
- `KEY `fk_products2` (`product_ID`)`
- `CONSTRAINT `fk_products2` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`
- `CONSTRAINT `fk_user1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### tbd_user_payment_methods

**Descripción.** Métodos de pago asociados a usuarios y a un tipo del catálogo. El par proveedor/referencia externa es único.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | Entero BIGINT de 64 bits sin signo (UNSIGNED). | Identificador técnico de la fila. | Cualitativa nominal; identificador/código | PK; NOT NULL; AUTO_INCREMENT | — |
| `user_ID` | `int` | Entero INT de 32 bits con signo. | Identificador de usuario; según la tabla es FK, parte de PK o clave UNIQUE. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tb_users`.`ID` |
| `payment_method_type_ID` | `int` | Entero INT de 32 bits con signo. | Tipo de método de pago; FK a tbc_payment_methods_types.ID. | Cualitativa nominal; identificador/código | FK; NOT NULL | `tbc_payment_methods_types`.`ID` |
| `provider` | `varchar(60)` | Cadena de longitud variable, máximo 60 caracteres; no se declara otro patrón. | Identificador textual del proveedor externo. | Cualitativa nominal; texto descriptivo | UNIQUE; NOT NULL | — |
| `provider_method_ref` | `varchar(255)` | Cadena de longitud variable, máximo 255 caracteres; no se declara otro patrón. | Referencia externa del método; junto con provider está sujeta a UNIQUE. | Cualitativa nominal; identificador/código | UNIQUE; NOT NULL | — |
| `label` | `varchar(100)` | Cadena de longitud variable, máximo 100 caracteres; no se declara otro patrón. | Etiqueta opcional para mostrar o reconocer el método de pago. | Cualitativa nominal; texto descriptivo | NULL; DEFAULT NULL | — |
| `last_four` | `char(4)` | Cadena de longitud fija de 4 caracteres. | Últimos cuatro caracteres del identificador de pago, en formato textual. | Cualitativa nominal; identificador/código | NULL; DEFAULT NULL | — |
| `is_default` | `tinyint(1)` | Entero de 8 bits declarado tinyint(1); no es un booleano estricto. | Indicador numérico 0/1 de dirección o método predeterminado; tinyint(1) no constituye por sí solo una restricción booleana. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT '0' | — |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NULL; DEFAULT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_provider_method` (`provider`,`provider_method_ref`)`
- `KEY `user_ID` (`user_ID`)`
- `KEY `payment_method_type_ID` (`payment_method_type_ID`)`
- `CONSTRAINT `tbd_user_payment_methods_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `tbd_user_payment_methods_ibfk_2` FOREIGN KEY (`payment_method_type_ID`) REFERENCES `tbc_payment_methods_types` (`ID`)`

### tbd_users_wishlist_products

**Descripción.** Tabla puente de productos guardados por usuarios en listas de deseos, con estado y fechas.

**Filas incluidas en SQL:** 0.

| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |
|---|---|---|---|---|---|---|
| `user_ID` | `int` | Entero INT de 32 bits con signo. | Identificador de usuario; según la tabla es FK, parte de PK o clave UNIQUE. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tb_users`.`ID` |
| `product_ID` | `int unsigned` | Entero INT de 32 bits sin signo (UNSIGNED). | Identificador del producto; puede ser FK, parte de PK compuesta o ambas según la tabla. | Cualitativa nominal; identificador/código | PK; FK; NOT NULL | `tb_products`.`ID` |
| `status` | `bit(1)` | Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación. | Indicador binario de estado; el esquema no define el significado funcional de 0 y 1. | Cualitativa nominal; categoría/indicador | NOT NULL; DEFAULT b'1' | — |
| `creation_date` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de creación del registro. | Temporal; fecha y hora (escala no asignada) | NOT NULL; DEFAULT CURRENT_TIMESTAMP | — |
| `last_update` | `datetime` | Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria. | Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente. | Temporal; fecha y hora (escala no asignada) | NOT NULL; ON UPDATE CURRENT_TIMESTAMP | — |

**Restricciones e índices de tabla (DDL):**

- `PRIMARY KEY (`user_ID`,`product_ID`)`
- `KEY `fk_products3` (`product_ID`)`
- `CONSTRAINT `fk_products3` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`
- `CONSTRAINT `fk_user2` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

## Relaciones entre tablas

| Estado | Nombre FK | Origen | Destino | Cardinalidad | Reglas |
|---|---|---|---|---|---|
| Declarada en DDL | `tb_buyer_orders_ibfk_1` | `tb_buyer_orders.seller_ID` | `tb_users.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tb_carts_ibfk_1` | `tb_carts.user_ID` | `tb_users.ID` | 1:1 (FK UNIQUE) | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_addresses_users` | `tb_user_addresses.user_ID` | `tb_users.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_superior_category` | `tbc_categories.sup_id_category` | `tbc_categories.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_component_address` | `tbd_address_components.address_ID` | `tb_user_addresses.ID` | N:1 desde origen; 1:N desde destino | ON DELETE RESTRICT |
| Declarada en DDL | `fk_component_parent` | `tbd_address_components.address_ID,address_sup_ID` | `tbd_address_components.address_ID,ID` | N:1 desde origen; 1:N desde destino | ON DELETE RESTRICT |
| Declarada en DDL | `tbd_carts_items_ibfk_1` | `tbd_carts_items.cart_ID` | `tb_carts.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_carts_items_ibfk_2` | `tbd_carts_items.provider_ID` | `tbd_products_users_providers.user_ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_carts_items_ibfk_3` | `tbd_carts_items.product_ID` | `tbd_products_users_providers.product_ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_order_items_ibfk_1` | `tbd_order_items.seller_order_ID` | `tb_buyer_orders.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_order_items_ibfk_2` | `tbd_order_items.product_ID` | `tbd_products_users_providers.product_ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_order_items_ibfk_3` | `tbd_order_items.provider_ID` | `tbd_products_users_providers.user_ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_tbd_pc_category` | `tbd_products_categories.categories_ID` | `tbc_categories.ID` | N:1 desde origen; 1:N desde destino | ON DELETE CASCADE ON UPDATE CASCADE |
| Declarada en DDL | `fk_tbd_pc_product` | `tbd_products_categories.product_ID` | `tb_products.ID` | N:1 desde origen; 1:N desde destino | ON DELETE CASCADE ON UPDATE CASCADE |
| Declarada en DDL | `fk_products2` | `tbd_products_users_providers.product_ID` | `tb_products.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_user1` | `tbd_products_users_providers.user_ID` | `tb_users.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_user_payment_methods_ibfk_1` | `tbd_user_payment_methods.user_ID` | `tb_users.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `tbd_user_payment_methods_ibfk_2` | `tbd_user_payment_methods.payment_method_type_ID` | `tbc_payment_methods_types.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_products3` | `tbd_users_wishlist_products.product_ID` | `tb_products.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Declarada en DDL | `fk_user2` | `tbd_users_wishlist_products.user_ID` | `tb_users.ID` | N:1 desde origen; 1:N desde destino | ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto). |
| Inferida; no FK | `inferida_product_id` | `tb_logs.product_id` | `tb_products.ID` | Candidata N:1; sin integridad FK | Sin FOREIGN KEY; inferencia por nombre y semántica de trazabilidad. Pendiente de validar. |

Las tablas puente forman relaciones muchos a muchos: productos-categorías, usuarios-productos/proveedores, usuarios-lista de deseos y carrito-producto-proveedor. `tbd_address_components` contiene una jerarquía autorreferente limitada a la misma dirección. La FK compuesta para líneas de carrito/pedido relaciona `provider_ID` y `product_ID` por separado en el DDL; la integridad efectiva depende de ambas restricciones y de las claves referenciadas.

## Vistas

Las vistas no tienen filas INSERT propias en el respaldo; su resultado depende de la consulta al ejecutarlas.

- `vw_total_products_by_category`
- `vw_trazabilidad_categorias`
- `vw_trazabilidad_categorizacion_productos`
- `vw_trazabilidad_productos`
- `vw_trazabilidad_usuarios`

## Procedimientos y triggers

**Procedimientos:** `sp_reactivar_product`, `sp_retiro_product`

**Triggers:** `trg_address_components_after_delete`, `trg_address_components_after_insert`, `trg_address_components_after_update`, `trg_buyer_orders_after_delete`, `trg_buyer_orders_after_insert`, `trg_buyer_orders_after_update`, `trg_carts_after_delete`, `trg_carts_after_insert`, `trg_carts_after_update`, `trg_carts_items_after_delete`, `trg_carts_items_after_insert`, `trg_carts_items_after_update`, `trg_categories_after_delete`, `trg_categories_after_insert`, `trg_categories_after_update`, `trg_order_items_after_delete`, `trg_order_items_after_insert`, `trg_order_items_after_update`, `trg_payment_methods_types_after_delete`, `trg_payment_methods_types_after_insert`, `trg_payment_methods_types_after_update`, `trg_products_after_delete`, `trg_products_after_insert`, `trg_products_after_update`, `trg_products_categories_after_delete`, `trg_products_categories_after_insert`, `trg_products_categories_after_update`, `trg_user_addresses_after_delete`, `trg_user_addresses_after_insert`, `trg_user_addresses_after_update`, `trg_user_payment_methods_after_delete`, `trg_user_payment_methods_after_insert`, `trg_user_payment_methods_after_update`, `trg_users_after_delete`, `trg_users_after_insert`, `trg_users_after_update`, `trg_users_wishlist_products_after_delete`, `trg_users_wishlist_products_after_insert`, `trg_users_wishlist_products_after_update`

## Criterios y límites

- Los conteos se obtuvieron contando tuplas INSERT del archivo SQL y se refieren exclusivamente al respaldo.
- `NULL`, `DEFAULT`, `AUTO_INCREMENT`, índices y restricciones se copiaron del DDL. Las restricciones CHECK y los índices completos se listan por tabla.
- La clasificación cualitativa/cuantitativa describe el uso semántico inferido; identificadores numéricos se clasifican como cualitativos nominales.
- Los campos sin descripción explícita en el DDL se interpretan por su nombre. Las referencias no declaradas se identifican como inferencias.
- Las vistas no tienen un total de registros estático dentro del respaldo.
- Los ejemplos son esquemáticos, no datos del respaldo; se omite el contenido de `password`.
