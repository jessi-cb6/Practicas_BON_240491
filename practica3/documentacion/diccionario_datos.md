# Diccionario de datos · db_test_7b

**Fuente:** `respaldos/practica3_terminada2.sql`  
**Motor:** MySQL 8.0 · **Tablas:** 26 · **Columnas:** 203 · **Filas en respaldo:** 128,893

Los conteos son las filas incluidas en los INSERT del respaldo; no representan una consulta al servidor activo.

## Resumen

| Tabla | Área | Columnas | Filas | Descripción |
|---|---|---:|---:|---|
| `tb_buyer_orders` | ventas | 8 | 0 | Cabecera de pedidos recibidos por un vendedor, con importes y etapa de cumplimiento. |
| `tb_carts` | ventas | 5 | 0 | Carrito de compra asociado a una cuenta de usuario. |
| `tb_logs` | auditoria | 8 | 91,770 | Bitácora de operaciones y cambios registrados en las entidades. |
| `tb_order_cancellations` | ventas | 7 | 0 | Entidad del modelo relacional. |
| `tb_orders` | ventas | 8 | 0 | Entidad del modelo relacional. |
| `tb_payment_methods` | pagos | 7 | 0 | Entidad del modelo relacional. |
| `tb_payment_transaction` | pagos | 10 | 0 | Entidad del modelo relacional. |
| `tb_payments` | pagos | 9 | 0 | Entidad del modelo relacional. |
| `tb_people` | cuentas | 12 | 7,502 | Entidad del modelo relacional. |
| `tb_products` | catalogo | 9 | 7,008 | Catálogo de productos, precios vigentes, existencias y disponibilidad. |
| `tb_refunds` | pagos | 9 | 0 | Entidad del modelo relacional. |
| `tb_returns` | pagos | 7 | 0 | Entidad del modelo relacional. |
| `tb_shipments` | pagos | 9 | 0 | Entidad del modelo relacional. |
| `tb_user_addresses` | cuentas | 12 | 0 | Direcciones de envío y contacto asociadas a usuarios. |
| `tb_users` | cuentas | 8 | 7,513 | Cuentas de usuario, acceso y estado de la cuenta. |
| `tbc_categories` | catalogo | 7 | 100 | Catálogo jerárquico de categorías de productos. |
| `tbc_payment_methods_types` | pagos | 6 | 0 | Catálogo de tipos de métodos de pago admitidos. |
| `tbd_address_components` | cuentas | 8 | 0 | Componentes jerárquicos que desglosan una dirección. |
| `tbd_cancellation_items` | ventas | 5 | 0 | Entidad del modelo relacional. |
| `tbd_cart_items` | ventas | 6 | 0 | Entidad del modelo relacional. |
| `tbd_order_items` | ventas | 9 | 0 | Detalle histórico de productos, cantidades y precios por pedido. |
| `tbd_products_categories` | catalogo | 5 | 15,000 | Tabla puente entre productos y categorías. |
| `tbd_products_users_providers` | proveedores | 7 | 0 | Relación de productos con usuarios proveedores o distribuidores. |
| `tbd_return_items` | ventas | 6 | 0 | Entidad del modelo relacional. |
| `tbd_user_payment_methods` | pagos | 11 | 0 | Métodos de pago registrados para los usuarios. |
| `tbd_users_wishlist_products` | proveedores | 5 | 0 | Productos guardados por usuarios en listas de deseos. |

## Diccionario por tabla

### `tb_buyer_orders`

Cabecera de pedidos recibidos por un vendedor, con importes y etapa de cumplimiento.

**Filas del respaldo:** 0 · **Columnas:** 8

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `seller_ID` | `int` | No | FK | — | Identificador del usuario vendedor. |
| `subtotal` | `decimal(12,2)` | No | — | `'0.00'` | Importe subtotal calculado o almacenado para la operación. |
| `shipping_cost` | `decimal(12,2)` | No | — | `'0.00'` | Importe del costo de envío. |
| `fulfillment_status` | `enum('Pending','Accepted','Preparing','Sent','Delivered','Canceled','Returned')` | No | — | `'Pending'` | Etapa de preparación y entrega del pedido. Valores: `Pending`, `Accepted`, `Preparing`, `Sent`, `Delivered`, `Canceled`, `Returned`. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `seller_ID` (`seller_ID`)`
- `CONSTRAINT `tb_buyer_orders_ibfk_1` FOREIGN KEY (`seller_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `tb_buyer_orders_chk_1` CHECK ((`subtotal` >= 0))`
- `CONSTRAINT `tb_buyer_orders_chk_2` CHECK ((`shipping_cost` >= 0))`

### `tb_carts`

Carrito de compra asociado a una cuenta de usuario.

**Filas del respaldo:** 0 · **Columnas:** 5

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `user_ID` | `int` | No | FK, UK | — | Identificador del usuario asociado. |
| `status` | `bit(1)` | Sí | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_cart_user` (`user_ID`)`
- `CONSTRAINT `tb_carts_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tb_logs`

Bitácora de operaciones y cambios registrados en las entidades.

**Filas del respaldo:** 91,770 · **Columnas:** 8

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int` | No | PK | — | Identificador técnico de la fila. |
| `table_name` | `varchar(80)` | No | — | — | Entidad o tabla afectada por el evento auditado. |
| `table_operation` | `enum('Create','Read','Update','Delete')` | Sí | — | `NULL` | Tipo de operación registrada en la bitácora. Valores: `Create`, `Read`, `Update`, `Delete`. |
| `db_user` | `varchar(80)` | No | — | — | Usuario de base de datos consignado como actor. |
| `operation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora en que se registró el evento. |
| `operation_description` | `text` | No | — | — | Descripción del evento de auditoría. |
| `operation_status` | `bit(1)` | Sí | — | `b'1'` | Indicador binario del resultado registrado. |
| `product_id` | `int unsigned` | Sí | — | `NULL` | Identificador relacionado con el evento; el respaldo no declara una FK para este campo. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_logs_table_op_date` (`table_name`,`table_operation`,`operation_date`)`
- `KEY `idx_logs_product_trace` (`table_name`,`table_operation`,`product_id`)`
- `KEY `idx_logs_tabla_operacion` (`table_name`,`table_operation`)`
- `KEY `idx_logs_table_op` (`table_name`,`table_operation`)`

### `tb_order_cancellations`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 7

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `order_ID` | `int unsigned` | No | FK | — | Referencia a tb_orders.ID. |
| `requested_by` | `int` | No | FK | — | Referencia a tb_users.ID. |
| `reason` | `varchar(500)` | No | — | — | Dato reason asociado a tb order cancellations; descripción inferida del nombre y tipo SQL. |
| `cancellation_status` | `enum('Requested','Approved','Rejected','Completed')` | No | — | `'Requested'` | Dato cancellation status asociado a tb order cancellations; descripción inferida del nombre y tipo SQL. Valores: `Requested`, `Approved`, `Rejected`, `Completed`. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb order cancellations; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb order cancellations; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_cancellations_order` (`order_ID`)`
- `KEY `idx_cancellations_user` (`requested_by`)`
- `CONSTRAINT `fk_cancellations_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`)`
- `CONSTRAINT `fk_cancellations_user` FOREIGN KEY (`requested_by`) REFERENCES `tb_users` (`ID`)`

### `tb_orders`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 8

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `buyer_ID` | `int` | No | FK | — | Referencia a tb_users.ID. |
| `shipping_address_ID` | `bigint unsigned` | Sí | FK | `NULL` | Referencia a tb_user_addresses.ID. |
| `subtotal` | `decimal(12,2)` | No | — | `'0.00'` | Importe subtotal calculado o almacenado para la operación. |
| `shipping_cost` | `decimal(12,2)` | No | — | `'0.00'` | Importe del costo de envío. |
| `order_status` | `enum('Pending','Paid','Processing','Shipped','Delivered','Canceled','Returned')` | No | — | `'Pending'` | Dato order status asociado a tb orders; descripción inferida del nombre y tipo SQL. Valores: `Pending`, `Paid`, `Processing`, `Shipped`, `Delivered`, `Canceled`, `Returned`. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb orders; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb orders; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_orders_buyer_created` (`buyer_ID`,`created_at`)`
- `KEY `idx_orders_address` (`shipping_address_ID`)`
- `CONSTRAINT `fk_orders_address` FOREIGN KEY (`shipping_address_ID`) REFERENCES `tb_user_addresses` (`ID`)`
- `CONSTRAINT `fk_orders_buyer` FOREIGN KEY (`buyer_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `chk_orders_amounts` CHECK (((`subtotal` >= 0) and (`shipping_cost` >= 0)))`

### `tb_payment_methods`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 7

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `code` | `varchar(40)` | No | UK | — | Dato code asociado a tb payment methods; descripción inferida del nombre y tipo SQL. |
| `name` | `varchar(100)` | No | — | — | Nombre visible del producto, categoría o elemento. |
| `description` | `varchar(500)` | Sí | — | `NULL` | Descripción textual complementaria. |
| `is_active` | `tinyint(1)` | No | — | `'1'` | Dato is active asociado a tb payment methods; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb payment methods; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb payment methods; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_payment_methods_code` (`code`)`
- `KEY `idx_payment_methods_active` (`is_active`)`

### `tb_payment_transaction`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 10

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `payment_ID` | `bigint unsigned` | No | FK | — | Referencia a tb_payments.ID. |
| `transaction_ref` | `varchar(150)` | No | UK | — | Dato transaction ref asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. |
| `transaction_type` | `enum('Authorize','Capture','Void','Charge','Refund')` | No | — | — | Dato transaction type asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. Valores: `Authorize`, `Capture`, `Void`, `Charge`, `Refund`. |
| `transaction_status` | `enum('Pending','Succeeded','Failed')` | No | — | `'Pending'` | Dato transaction status asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. Valores: `Pending`, `Succeeded`, `Failed`. |
| `amount` | `decimal(12,2)` | No | — | — | Dato amount asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. |
| `gateway` | `varchar(80)` | Sí | — | `NULL` | Dato gateway asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. |
| `response_code` | `varchar(80)` | Sí | — | `NULL` | Dato response code asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb payment transaction; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_payment_transaction_ref` (`transaction_ref`)`
- `KEY `idx_payment_transaction_payment_date` (`payment_ID`,`created_at`)`
- `CONSTRAINT `fk_payment_transaction_payment` FOREIGN KEY (`payment_ID`) REFERENCES `tb_payments` (`ID`)`
- `CONSTRAINT `chk_payment_transaction_amount` CHECK ((`amount` >= 0))`

### `tb_payments`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 9

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `order_ID` | `int unsigned` | No | FK | — | Referencia a tb_orders.ID. |
| `payment_method_ID` | `int unsigned` | Sí | FK | `NULL` | Referencia a tb_payment_methods.ID. |
| `amount` | `decimal(12,2)` | No | — | — | Dato amount asociado a tb payments; descripción inferida del nombre y tipo SQL. |
| `currency` | `char(3)` | No | — | `'MXN'` | Dato currency asociado a tb payments; descripción inferida del nombre y tipo SQL. |
| `payment_status` | `enum('Pending','Authorized','Paid','Failed','PartiallyRefunded','Refunded')` | No | — | `'Pending'` | Dato payment status asociado a tb payments; descripción inferida del nombre y tipo SQL. Valores: `Pending`, `Authorized`, `Paid`, `Failed`, `PartiallyRefunded`, `Refunded`. |
| `paid_at` | `datetime` | Sí | — | `NULL` | Dato paid at asociado a tb payments; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb payments; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb payments; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_payments_order` (`order_ID`)`
- `KEY `idx_payments_method` (`payment_method_ID`)`
- `KEY `idx_payments_status_created` (`payment_status`,`created_at`)`
- `CONSTRAINT `fk_payments_method` FOREIGN KEY (`payment_method_ID`) REFERENCES `tb_payment_methods` (`ID`)`
- `CONSTRAINT `fk_payments_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`)`
- `CONSTRAINT `chk_payments_amount` CHECK ((`amount` >= 0))`

### `tb_people`

Entidad del modelo relacional.

**Filas del respaldo:** 7,502 · **Columnas:** 12

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `person_ID` | `bigint` | No | PK | — | Identificador del perfil personal asociado. |
| `user_ID` | `int` | Sí | FK, UK | `NULL` | Identificador del usuario asociado. |
| `courtesy_title` | `varchar(20)` | Sí | — | `NULL` | Dato courtesy title asociado a tb people; descripción inferida del nombre y tipo SQL. |
| `given_names` | `varchar(150)` | No | — | — | Dato given names asociado a tb people; descripción inferida del nombre y tipo SQL. |
| `family_names` | `varchar(150)` | Sí | — | `NULL` | Dato family names asociado a tb people; descripción inferida del nombre y tipo SQL. |
| `birth_date` | `date` | Sí | — | `NULL` | Fecha de nacimiento del perfil personal. |
| `gender` | `enum('Hombre','Mujer','Prefiero no decirlo')` | No | — | `'Prefiero no decirlo'` | Género declarado en el perfil personal. Valores: `Hombre`, `Mujer`, `Prefiero no decirlo`. |
| `country_code` | `char(2)` | Sí | — | `NULL` | Código de país asociado al perfil o teléfono. |
| `phone` | `varchar(25)` | Sí | — | `NULL` | Número telefónico de contacto. |
| `status` | `bit(1)` | Sí | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | Sí | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `CURRENT_TIMESTAMP` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`person_ID`)`
- `UNIQUE KEY `user_ID` (`user_ID`)`
- `CONSTRAINT `fk_people_users` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tb_products`

Catálogo de productos, precios vigentes, existencias y disponibilidad.

**Filas del respaldo:** 7,008 · **Columnas:** 9

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `SKU` | `varchar(50)` | No | UK | — | Código comercial único del producto. |
| `name` | `varchar(250)` | No | — | — | Nombre visible del producto, categoría o elemento. |
| `description` | `text` | Sí | — | — | Descripción textual complementaria. |
| `current_price` | `decimal(10,2)` | No | — | `'0.00'` | Precio vigente del producto. |
| `current_stock` | `int unsigned` | No | — | `'0'` | Unidades registradas actualmente en existencia. |
| `status` | `bit(1)` | Sí | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `SKU` (`SKU`)`

### `tb_refunds`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 9

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `payment_ID` | `bigint unsigned` | No | FK | — | Referencia a tb_payments.ID. |
| `return_ID` | `bigint unsigned` | Sí | FK | `NULL` | Referencia a tb_returns.ID. |
| `amount` | `decimal(12,2)` | No | — | — | Dato amount asociado a tb refunds; descripción inferida del nombre y tipo SQL. |
| `refund_status` | `enum('Pending','Processing','Succeeded','Failed')` | No | — | `'Pending'` | Dato refund status asociado a tb refunds; descripción inferida del nombre y tipo SQL. Valores: `Pending`, `Processing`, `Succeeded`, `Failed`. |
| `reason` | `varchar(500)` | Sí | — | `NULL` | Dato reason asociado a tb refunds; descripción inferida del nombre y tipo SQL. |
| `refunded_at` | `datetime` | Sí | — | `NULL` | Dato refunded at asociado a tb refunds; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb refunds; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb refunds; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_refunds_payment` (`payment_ID`)`
- `KEY `idx_refunds_return` (`return_ID`)`
- `KEY `idx_refunds_status` (`refund_status`)`
- `CONSTRAINT `fk_refunds_payment` FOREIGN KEY (`payment_ID`) REFERENCES `tb_payments` (`ID`)`
- `CONSTRAINT `fk_refunds_return` FOREIGN KEY (`return_ID`) REFERENCES `tb_returns` (`ID`)`
- `CONSTRAINT `chk_refunds_amount` CHECK ((`amount` > 0))`

### `tb_returns`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 7

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `order_ID` | `int unsigned` | No | FK | — | Referencia a tb_orders.ID. |
| `requested_by` | `int` | No | FK | — | Referencia a tb_users.ID. |
| `return_status` | `enum('Requested','Approved','Rejected','InTransit','Received','Completed')` | No | — | `'Requested'` | Dato return status asociado a tb returns; descripción inferida del nombre y tipo SQL. Valores: `Requested`, `Approved`, `Rejected`, `InTransit`, `Received`, `Completed`. |
| `reason` | `varchar(500)` | No | — | — | Dato reason asociado a tb returns; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb returns; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb returns; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_returns_order` (`order_ID`)`
- `KEY `idx_returns_user` (`requested_by`)`
- `KEY `idx_returns_status` (`return_status`)`
- `CONSTRAINT `fk_returns_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`)`
- `CONSTRAINT `fk_returns_user` FOREIGN KEY (`requested_by`) REFERENCES `tb_users` (`ID`)`

### `tb_shipments`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 9

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `order_ID` | `int unsigned` | No | FK | — | Referencia a tb_orders.ID. |
| `carrier` | `varchar(100)` | Sí | — | `NULL` | Dato carrier asociado a tb shipments; descripción inferida del nombre y tipo SQL. |
| `tracking_number` | `varchar(150)` | Sí | UK | `NULL` | Dato tracking number asociado a tb shipments; descripción inferida del nombre y tipo SQL. |
| `shipment_status` | `enum('Pending','Ready','InTransit','Delivered','Lost','Returned')` | No | — | `'Pending'` | Dato shipment status asociado a tb shipments; descripción inferida del nombre y tipo SQL. Valores: `Pending`, `Ready`, `InTransit`, `Delivered`, `Lost`, `Returned`. |
| `shipped_at` | `datetime` | Sí | — | `NULL` | Dato shipped at asociado a tb shipments; descripción inferida del nombre y tipo SQL. |
| `delivered_at` | `datetime` | Sí | — | `NULL` | Dato delivered at asociado a tb shipments; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tb shipments; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tb shipments; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_shipments_tracking` (`tracking_number`)`
- `KEY `idx_shipments_order` (`order_ID`)`
- `KEY `idx_shipments_status` (`shipment_status`)`
- `CONSTRAINT `fk_shipments_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`)`

### `tb_user_addresses`

Direcciones de envío y contacto asociadas a usuarios.

**Filas del respaldo:** 0 · **Columnas:** 12

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `user_ID` | `int` | No | FK | — | Identificador del usuario asociado. |
| `address_label` | `varchar(100)` | No | — | — | Dato address label asociado a tb user addresses; descripción inferida del nombre y tipo SQL. |
| `recipient_name` | `varchar(150)` | Sí | — | `NULL` | Dato recipient name asociado a tb user addresses; descripción inferida del nombre y tipo SQL. |
| `recipient_phone` | `varchar(25)` | Sí | — | `NULL` | Dato recipient phone asociado a tb user addresses; descripción inferida del nombre y tipo SQL. |
| `delivery_instructions` | `varchar(500)` | Sí | — | `NULL` | Dato delivery instructions asociado a tb user addresses; descripción inferida del nombre y tipo SQL. |
| `latitude` | `decimal(10,7)` | Sí | — | `NULL` | Coordenada geográfica de latitud. |
| `longitude` | `decimal(10,7)` | Sí | — | `NULL` | Coordenada geográfica de longitud. |
| `is_default` | `tinyint(1)` | No | — | `'0'` | Indicador de selección predeterminada. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `idx_user_addresses` (`user_ID`)`
- `CONSTRAINT `fk_addresses_users` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `chk_coordinates` CHECK ((((`latitude` is null) and (`longitude` is null)) or ((`latitude` is not null) and (`longitude` is not null))))`
- `CONSTRAINT `chk_latitude` CHECK ((`latitude` between -(90) and 90))`
- `CONSTRAINT `chk_longitude` CHECK ((`longitude` between -(180) and 180))`

### `tb_users`

Cuentas de usuario, acceso y estado de la cuenta.

**Filas del respaldo:** 7,513 · **Columnas:** 8

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int` | No | PK | — | Identificador técnico de la fila. |
| `email` | `varchar(100)` | No | UK | — | Correo electrónico asociado a la cuenta. |
| `nick` | `varchar(50)` | No | UK | — | Alias o nombre corto de la cuenta. |
| `password` | `varchar(255)` | No | — | — | Campo de credencial; el DDL no especifica el mecanismo de protección. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |
| `last_login` | `datetime` | Sí | — | `NULL` | Fecha y hora del último inicio de sesión. |
| `status` | `bit(1)` | Sí | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `email` (`email`)`
- `UNIQUE KEY `nick` (`nick`)`

### `tbc_categories`

Catálogo jerárquico de categorías de productos.

**Filas del respaldo:** 100 · **Columnas:** 7

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `name` | `varchar(120)` | No | UK | — | Nombre visible del producto, categoría o elemento. |
| `description` | `text` | Sí | — | — | Descripción textual complementaria. |
| `sup_id_category` | `int unsigned` | Sí | FK | `NULL` | Categoría superior opcional; permite construir la jerarquía de categorías. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | — | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `name` (`name`)`
- `KEY `fk_superior_category` (`sup_id_category`)`
- `CONSTRAINT `fk_superior_category` FOREIGN KEY (`sup_id_category`) REFERENCES `tbc_categories` (`ID`)`

### `tbc_payment_methods_types`

Catálogo de tipos de métodos de pago admitidos.

**Filas del respaldo:** 0 · **Columnas:** 6

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int` | No | PK | — | Identificador técnico de la fila. |
| `code` | `varchar(30)` | No | UK | — | Dato code asociado a tbc payment methods types; descripción inferida del nombre y tipo SQL. |
| `description` | `text` | No | — | — | Descripción textual complementaria. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `code` (`code`)`

### `tbd_address_components`

Componentes jerárquicos que desglosan una dirección.

**Filas del respaldo:** 0 · **Columnas:** 8

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK, UK | — | Identificador técnico de la fila. |
| `address_ID` | `bigint unsigned` | No | FK, UK | — | Identificador de la dirección asociada. |
| `value` | `varchar(255)` | No | — | — | Dato value asociado a tbd address components; descripción inferida del nombre y tipo SQL. |
| `component_type` | `varchar(50)` | No | — | — | Tipo de componente que representa el valor de dirección. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `address_sup_ID` | `bigint unsigned` | Sí | FK | `NULL` | Componente superior opcional dentro de la misma dirección. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_address_component` (`address_ID`,`ID`)`
- `KEY `idx_address_parent` (`address_ID`,`address_sup_ID`)`
- `CONSTRAINT `fk_component_address` FOREIGN KEY (`address_ID`) REFERENCES `tb_user_addresses` (`ID`) ON DELETE RESTRICT`
- `CONSTRAINT `fk_component_parent` FOREIGN KEY (`address_ID`, `address_sup_ID`) REFERENCES `tbd_address_components` (`address_ID`, `ID`) ON DELETE RESTRICT`

### `tbd_cancellation_items`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 5

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `cancellation_ID` | `bigint unsigned` | No | PK, FK | — | Referencia a tb_order_cancellations.ID. |
| `order_item_ID` | `int unsigned` | No | PK, FK | — | Referencia a tbd_order_items.ID. |
| `quantity` | `int unsigned` | No | — | — | Cantidad de unidades del producto. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tbd cancellation items; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tbd cancellation items; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`cancellation_ID`,`order_item_ID`)`
- `KEY `idx_cancellation_items_order_item` (`order_item_ID`)`
- `CONSTRAINT `fk_cancellation_items_cancellation` FOREIGN KEY (`cancellation_ID`) REFERENCES `tb_order_cancellations` (`ID`)`
- `CONSTRAINT `fk_cancellation_items_order_item` FOREIGN KEY (`order_item_ID`) REFERENCES `tbd_order_items` (`ID`)`
- `CONSTRAINT `chk_cancellation_items_quantity` CHECK ((`quantity` > 0))`

### `tbd_cart_items`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 6

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `cart_ID` | `int unsigned` | No | PK, FK | — | Identificador del carrito asociado. |
| `provider_ID` | `int` | No | PK, FK | — | Identificador del usuario proveedor. |
| `product_ID` | `int unsigned` | No | PK, FK | — | Identificador del producto asociado. |
| `quantity` | `int unsigned` | No | — | `'1'` | Cantidad de unidades del producto. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tbd cart items; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tbd cart items; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`cart_ID`,`provider_ID`,`product_ID`)`
- `KEY `idx_cart_items_provider_product` (`provider_ID`,`product_ID`)`
- `CONSTRAINT `fk_cart_items_cart` FOREIGN KEY (`cart_ID`) REFERENCES `tb_carts` (`ID`)`
- `CONSTRAINT `fk_cart_items_provider_product` FOREIGN KEY (`provider_ID`, `product_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`, `product_ID`)`
- `CONSTRAINT `chk_cart_items_quantity` CHECK ((`quantity` > 0))`

### `tbd_order_items`

Detalle histórico de productos, cantidades y precios por pedido.

**Filas del respaldo:** 0 · **Columnas:** 9

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | — | Identificador técnico de la fila. |
| `seller_order_ID` | `int unsigned` | No | FK | — | Identificador del pedido de venta asociado. |
| `product_ID` | `int unsigned` | No | FK | — | Identificador del producto asociado. |
| `provider_ID` | `int` | No | FK | — | Identificador del usuario proveedor. |
| `product_name` | `varchar(255)` | No | — | — | Dato product name asociado a tbd order items; descripción inferida del nombre y tipo SQL. |
| `quantity` | `int unsigned` | No | — | — | Cantidad de unidades del producto. |
| `unit_price` | `decimal(12,2)` | No | — | — | Precio unitario aplicado en la operación. |
| `subtotal` | `decimal(12,2)` | Sí | — | — | Importe subtotal calculado o almacenado para la operación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `KEY `seller_order_ID` (`seller_order_ID`)`
- `KEY `product_ID` (`product_ID`)`
- `KEY `provider_ID` (`provider_ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_1` FOREIGN KEY (`seller_order_ID`) REFERENCES `tb_buyer_orders` (`ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_2` FOREIGN KEY (`product_ID`) REFERENCES `tbd_products_users_providers` (`product_ID`)`
- `CONSTRAINT `tbd_order_items_ibfk_3` FOREIGN KEY (`provider_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`)`
- `CONSTRAINT `tbd_order_items_chk_1` CHECK ((`quantity` > 0))`
- `CONSTRAINT `tbd_order_items_chk_2` CHECK ((`unit_price` >= 0))`

### `tbd_products_categories`

Tabla puente entre productos y categorías.

**Filas del respaldo:** 15,000 · **Columnas:** 5

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `product_ID` | `int unsigned` | No | PK, FK | — | Identificador del producto asociado. |
| `categories_ID` | `int unsigned` | No | PK, FK | — | Identificador de la categoría asociada. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`product_ID`,`categories_ID`)`
- `KEY `fk_tbd_pc_category` (`categories_ID`)`
- `KEY `idx_pc_producto_categoria` (`product_ID`,`categories_ID`)`
- `CONSTRAINT `fk_tbd_pc_category` FOREIGN KEY (`categories_ID`) REFERENCES `tbc_categories` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE`
- `CONSTRAINT `fk_tbd_pc_product` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE`

### `tbd_products_users_providers`

Relación de productos con usuarios proveedores o distribuidores.

**Filas del respaldo:** 0 · **Columnas:** 7

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `user_ID` | `int` | No | PK, FK | — | Identificador del usuario asociado. |
| `product_ID` | `int unsigned` | No | PK, FK | — | Identificador del producto asociado. |
| `type_ownership` | `enum('Owner','Reseller','Distributor')` | Sí | — | `NULL` | Rol del usuario con respecto al producto. Valores: `Owner`, `Reseller`, `Distributor`. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `available_date` | `datetime` | No | — | — | Fecha desde la que se declara disponible la relación producto-proveedor. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`user_ID`,`product_ID`)`
- `KEY `fk_products2` (`product_ID`)`
- `CONSTRAINT `fk_products2` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`
- `CONSTRAINT `fk_user1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

### `tbd_return_items`

Entidad del modelo relacional.

**Filas del respaldo:** 0 · **Columnas:** 6

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `return_ID` | `bigint unsigned` | No | PK, FK | — | Referencia a tb_returns.ID. |
| `order_item_ID` | `int unsigned` | No | PK, FK | — | Referencia a tbd_order_items.ID. |
| `quantity` | `int unsigned` | No | — | — | Cantidad de unidades del producto. |
| `condition_note` | `varchar(500)` | Sí | — | `NULL` | Dato condition note asociado a tbd return items; descripción inferida del nombre y tipo SQL. |
| `created_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato created at asociado a tbd return items; descripción inferida del nombre y tipo SQL. |
| `updated_at` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Dato updated at asociado a tbd return items; descripción inferida del nombre y tipo SQL. |

**Índices y restricciones**

- `PRIMARY KEY (`return_ID`,`order_item_ID`)`
- `KEY `idx_return_items_order_item` (`order_item_ID`)`
- `CONSTRAINT `fk_return_items_order_item` FOREIGN KEY (`order_item_ID`) REFERENCES `tbd_order_items` (`ID`)`
- `CONSTRAINT `fk_return_items_return` FOREIGN KEY (`return_ID`) REFERENCES `tb_returns` (`ID`)`
- `CONSTRAINT `chk_return_items_quantity` CHECK ((`quantity` > 0))`

### `tbd_user_payment_methods`

Métodos de pago registrados para los usuarios.

**Filas del respaldo:** 0 · **Columnas:** 11

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | — | Identificador técnico de la fila. |
| `user_ID` | `int` | No | FK | — | Identificador del usuario asociado. |
| `payment_method_type_ID` | `int` | No | FK | — | Identificador del tipo de método de pago. |
| `provider` | `varchar(60)` | No | UK | — | Proveedor o procesador externo del método de pago. |
| `provider_method_ref` | `varchar(255)` | No | UK | — | Referencia externa del método en el proveedor de pagos. |
| `label` | `varchar(100)` | Sí | — | `NULL` | Dato label asociado a tbd user payment methods; descripción inferida del nombre y tipo SQL. |
| `last_four` | `char(4)` | Sí | — | `NULL` | Últimos cuatro dígitos del medio de pago. |
| `is_default` | `tinyint(1)` | No | — | `'0'` | Indicador de selección predeterminada. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | `NULL` | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`ID`)`
- `UNIQUE KEY `uk_provider_method` (`provider`,`provider_method_ref`)`
- `KEY `user_ID` (`user_ID`)`
- `KEY `payment_method_type_ID` (`payment_method_type_ID`)`
- `CONSTRAINT `tbd_user_payment_methods_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`
- `CONSTRAINT `tbd_user_payment_methods_ibfk_2` FOREIGN KEY (`payment_method_type_ID`) REFERENCES `tbc_payment_methods_types` (`ID`)`

### `tbd_users_wishlist_products`

Productos guardados por usuarios en listas de deseos.

**Filas del respaldo:** 0 · **Columnas:** 5

| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |
|---|---|---|---|---|---|
| `user_ID` | `int` | No | PK, FK | — | Identificador del usuario asociado. |
| `product_ID` | `int unsigned` | No | PK, FK | — | Identificador del producto asociado. |
| `status` | `bit(1)` | No | — | `b'1'` | Indicador binario de estado; su significado exacto depende de la aplicación. |
| `creation_date` | `datetime` | No | — | `CURRENT_TIMESTAMP` | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | — | Fecha y hora de la última modificación. |

**Índices y restricciones**

- `PRIMARY KEY (`user_ID`,`product_ID`)`
- `KEY `fk_products3` (`product_ID`)`
- `CONSTRAINT `fk_products3` FOREIGN KEY (`product_ID`) REFERENCES `tb_products` (`ID`)`
- `CONSTRAINT `fk_user2` FOREIGN KEY (`user_ID`) REFERENCES `tb_users` (`ID`)`

## Relaciones

Las relaciones declaradas se derivan de FOREIGN KEY y se muestran desde la tabla que contiene la llave (N:1 hacia la tabla referenciada).

- **FK declarada:** `tb_buyer_orders.seller_ID` → `tb_users.ID`.
- **FK declarada:** `tb_carts.user_ID` → `tb_users.ID`.
- **FK declarada:** `tb_order_cancellations.order_ID` → `tb_orders.ID`.
- **FK declarada:** `tb_order_cancellations.requested_by` → `tb_users.ID`.
- **FK declarada:** `tb_orders.shipping_address_ID` → `tb_user_addresses.ID`.
- **FK declarada:** `tb_orders.buyer_ID` → `tb_users.ID`.
- **FK declarada:** `tb_payment_transaction.payment_ID` → `tb_payments.ID`.
- **FK declarada:** `tb_payments.payment_method_ID` → `tb_payment_methods.ID`.
- **FK declarada:** `tb_payments.order_ID` → `tb_orders.ID`.
- **FK declarada:** `tb_people.user_ID` → `tb_users.ID`.
- **FK declarada:** `tb_refunds.payment_ID` → `tb_payments.ID`.
- **FK declarada:** `tb_refunds.return_ID` → `tb_returns.ID`.
- **FK declarada:** `tb_returns.order_ID` → `tb_orders.ID`.
- **FK declarada:** `tb_returns.requested_by` → `tb_users.ID`.
- **FK declarada:** `tb_shipments.order_ID` → `tb_orders.ID`.
- **FK declarada:** `tb_user_addresses.user_ID` → `tb_users.ID`.
- **FK declarada:** `tbc_categories.sup_id_category` → `tbc_categories.ID`.
- **FK declarada:** `tbd_address_components.address_ID` → `tb_user_addresses.ID`.
- **FK declarada:** `tbd_address_components.address_ID, address_sup_ID` → `tbd_address_components.address_ID, ID`.
- **FK declarada:** `tbd_cancellation_items.cancellation_ID` → `tb_order_cancellations.ID`.
- **FK declarada:** `tbd_cancellation_items.order_item_ID` → `tbd_order_items.ID`.
- **FK declarada:** `tbd_cart_items.cart_ID` → `tb_carts.ID`.
- **FK declarada:** `tbd_cart_items.provider_ID, product_ID` → `tbd_products_users_providers.user_ID, product_ID`.
- **FK declarada:** `tbd_order_items.seller_order_ID` → `tb_buyer_orders.ID`.
- **FK declarada:** `tbd_order_items.product_ID` → `tbd_products_users_providers.product_ID`.
- **FK declarada:** `tbd_order_items.provider_ID` → `tbd_products_users_providers.user_ID`.
- **FK declarada:** `tbd_products_categories.categories_ID` → `tbc_categories.ID`.
- **FK declarada:** `tbd_products_categories.product_ID` → `tb_products.ID`.
- **FK declarada:** `tbd_products_users_providers.product_ID` → `tb_products.ID`.
- **FK declarada:** `tbd_products_users_providers.user_ID` → `tb_users.ID`.
- **FK declarada:** `tbd_return_items.order_item_ID` → `tbd_order_items.ID`.
- **FK declarada:** `tbd_return_items.return_ID` → `tb_returns.ID`.
- **FK declarada:** `tbd_user_payment_methods.user_ID` → `tb_users.ID`.
- **FK declarada:** `tbd_user_payment_methods.payment_method_type_ID` → `tbc_payment_methods_types.ID`.
- **FK declarada:** `tbd_users_wishlist_products.product_ID` → `tb_products.ID`.
- **FK declarada:** `tbd_users_wishlist_products.user_ID` → `tb_users.ID`.
- **Inferida; no es FK física:** `tb_logs.product_id` → `tb_products.ID`.

## Objetos del respaldo

- Vistas (25): `vw_total_products_by_category`, `vw_trazabilidad_address_components`, `vw_trazabilidad_cancellation_items`, `vw_trazabilidad_cart_items`, `vw_trazabilidad_carts`, `vw_trazabilidad_categorias`, `vw_trazabilidad_categorizacion_productos`, `vw_trazabilidad_order_cancellations`, `vw_trazabilidad_order_items`, `vw_trazabilidad_orders`, `vw_trazabilidad_payment_methods`, `vw_trazabilidad_payment_methods_types`, `vw_trazabilidad_payment_transaction`, `vw_trazabilidad_payments`, `vw_trazabilidad_people`, `vw_trazabilidad_productos`, `vw_trazabilidad_products_users_providers`, `vw_trazabilidad_refunds`, `vw_trazabilidad_return_items`, `vw_trazabilidad_returns`, `vw_trazabilidad_shipments`, `vw_trazabilidad_user_addresses`, `vw_trazabilidad_user_payment_methods`, `vw_trazabilidad_users_wishlist_products`, `vw_trazabilidad_usuarios`
- Procedimientos (3): `sp_reactivar_product`, `sp_register_new_user`, `sp_retiro_product`
- Triggers: 72

**Validación del análisis:** 69 sentencias INSERT; 128,893 filas contabilizadas y asociadas a tablas del respaldo.
