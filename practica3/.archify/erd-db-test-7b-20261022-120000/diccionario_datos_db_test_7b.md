# Diccionario de datos — db_test_7b

Fuente: `respaldos/respaldo_final_22_10_2026.sql` · 16 tablas · 55,260 filas en el respaldo.

Los conteos son filas contenidas en las sentencias `INSERT` del archivo, no conteos de una instancia activa. Las descripciones funcionales se derivan del nombre, tipo y contexto del campo porque el dump no incluye comentarios `COMMENT` para las columnas.

## Resumen de registros

| Tabla | Registros | Columnas |
|---|---:|---:|
| `tb_buyer_orders` | 0 | 8 |
| `tb_carts` | 0 | 5 |
| `tb_logs` | 30,140 | 8 |
| `tb_people` | 7,502 | 12 |
| `tb_products` | 5,007 | 9 |
| `tb_user_addresses` | 0 | 12 |
| `tb_users` | 7,513 | 8 |
| `tbc_categories` | 100 | 7 |
| `tbc_payment_methods_types` | 0 | 6 |
| `tbd_address_components` | 0 | 8 |
| `tbd_carts_items` | 0 | 5 |
| `tbd_order_items` | 0 | 9 |
| `tbd_products_categories` | 4,998 | 5 |
| `tbd_products_users_providers` | 0 | 7 |
| `tbd_user_payment_methods` | 0 | 11 |
| `tbd_users_wishlist_products` | 0 | 5 |

## Definición de tablas

### `tb_buyer_orders`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | Identificador único del registro. |
| `seller_ID` | `int` | No | FK | Usuario vendedor responsable de la orden. |
| `subtotal` | `decimal(12,2)` | No | — | Importe subtotal de la orden o línea. |
| `shipping_cost` | `decimal(12,2)` | No | — | Costo de envío de la orden. |
| `fulfillment_status` | `enum('Pending','Accepted','Preparing','Sent','Delivered','Canceled','Returned')` | No | — | Estado del proceso de preparación y entrega. |
| `status` | `bit(1)` | No | — | Indicador de vigencia de la orden. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tb_carts`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | Identificador único del registro. |
| `user_ID` | `int` | No | FK, UK | Usuario propietario o asociado al registro. |
| `status` | `bit(1)` | Sí | — | Indicador de vigencia del carrito. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tb_logs`

Registros en el respaldo: **30,140**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int` | No | PK | Identificador único del registro. |
| `table_name` | `varchar(80)` | No | — | Nombre de la tabla afectada por la operación registrada. |
| `table_operation` | `enum('Create','Read','Update','Delete')` | Sí | — | Tipo de operación registrada sobre la base de datos. |
| `db_user` | `varchar(80)` | No | — | Usuario de base de datos que ejecutó la operación. |
| `operation_date` | `datetime` | No | — | Fecha y hora en que se registró la operación. |
| `operation_description` | `text` | No | — | Detalle textual de la operación auditada. |
| `operation_status` | `bit(1)` | Sí | — | Resultado o estado de la operación auditada. |
| `product_id` | `int unsigned` | Sí | — | Identificador de producto relacionado con el evento; el dump no declara FK. |

### `tb_people`

Registros en el respaldo: **7,502**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `person_ID` | `bigint` | No | PK | Identificador único del perfil personal. |
| `user_ID` | `int` | Sí | FK, UK | Usuario propietario o asociado al registro. |
| `courtesy_title` | `varchar(20)` | Sí | — | Tratamiento o título de cortesía de la persona. |
| `given_names` | `varchar(150)` | No | — | Nombres de la persona. |
| `family_names` | `varchar(150)` | Sí | — | Apellidos de la persona. |
| `birth_date` | `date` | Sí | — | Fecha de nacimiento de la persona. |
| `gender` | `enum('Hombre','Mujer','Prefiero no decirlo')` | No | — | Género declarado por la persona. |
| `country_code` | `char(2)` | Sí | — | Código de país asociado al teléfono o perfil. |
| `phone` | `varchar(25)` | Sí | — | Número telefónico de contacto de la persona. |
| `status` | `bit(1)` | Sí | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | Sí | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tb_products`

Registros en el respaldo: **5,007**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | Identificador único del registro. |
| `SKU` | `varchar(50)` | No | UK | Código de identificación comercial del producto. |
| `name` | `varchar(250)` | No | — | Nombre comercial del producto. |
| `description` | `text` | Sí | — | Descripción textual del producto, categoría o tipo. |
| `current_price` | `decimal(10,2)` | No | — | Precio vigente del producto. |
| `current_stock` | `int unsigned` | No | — | Existencia actual del producto. |
| `status` | `bit(1)` | Sí | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | Fecha y hora de la última modificación. |

### `tb_user_addresses`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | Identificador único del registro. |
| `user_ID` | `int` | No | FK | Usuario propietario o asociado al registro. |
| `address_label` | `varchar(100)` | No | — | Etiqueta que identifica la dirección para el usuario. |
| `recipient_name` | `varchar(150)` | Sí | — | Nombre de la persona que recibirá el envío. |
| `recipient_phone` | `varchar(25)` | Sí | — | Teléfono de contacto del destinatario. |
| `delivery_instructions` | `varchar(500)` | Sí | — | Indicaciones para entregar en la dirección. |
| `latitude` | `decimal(10,7)` | Sí | — | Coordenada geográfica de latitud. |
| `longitude` | `decimal(10,7)` | Sí | — | Coordenada geográfica de longitud. |
| `is_default` | `tinyint(1)` | No | — | Indica si es la opción predeterminada. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tb_users`

Registros en el respaldo: **7,513**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int` | No | PK | Identificador único del registro. |
| `email` | `varchar(100)` | No | UK | Correo electrónico de acceso o contacto del usuario. |
| `nick` | `varchar(50)` | No | UK | Nombre corto o alias del usuario. |
| `password` | `varchar(255)` | No | — | Credencial de autenticación almacenada. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |
| `last_login` | `datetime` | Sí | — | Fecha y hora del último inicio de sesión. |
| `status` | `bit(1)` | Sí | — | Indicador de vigencia o habilitación del registro. |

### `tbc_categories`

Registros en el respaldo: **100**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | Identificador único del registro. |
| `name` | `varchar(120)` | No | UK | Nombre visible del producto o categoría. |
| `description` | `text` | Sí | — | Descripción textual del producto, categoría o tipo. |
| `sup_id_category` | `int unsigned` | Sí | FK | Categoría superior; permite organizar categorías jerárquicamente. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | Fecha y hora de la última modificación. |

### `tbc_payment_methods_types`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int` | No | PK | Identificador único del registro. |
| `code` | `varchar(30)` | No | UK | Código único o abreviado del tipo de método de pago. |
| `description` | `text` | No | — | Descripción textual del producto, categoría o tipo. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tbd_address_components`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK, UK | Identificador único del registro. |
| `address_ID` | `bigint unsigned` | No | FK, UK | Dirección a la que pertenece el componente. |
| `value` | `varchar(255)` | No | — | Valor textual del componente de dirección. |
| `component_type` | `varchar(50)` | No | — | Clase de componente de dirección (por ejemplo, calle o ciudad). |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `address_sup_ID` | `bigint unsigned` | Sí | FK | Componente superior de esta jerarquía de dirección. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tbd_carts_items`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `cart_ID` | `int unsigned` | No | PK, FK | Carrito al que pertenece el artículo. |
| `provider_ID` | `int` | No | PK, FK | Usuario proveedor asociado al artículo. |
| `product_ID` | `int unsigned` | No | PK, FK | Producto asociado al registro. |
| `quantity` | `int unsigned` | No | — | Cantidad de unidades del producto. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |

### `tbd_order_items`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `int unsigned` | No | PK | Identificador único del registro. |
| `seller_order_ID` | `int unsigned` | No | FK | Orden de venta a la que pertenece el detalle. |
| `product_ID` | `int unsigned` | No | FK | Producto asociado al registro. |
| `provider_ID` | `int` | No | FK | Usuario proveedor asociado al artículo. |
| `product_name` | `varchar(255)` | No | — | Atributo product name asociado a tbd order items; significado inferido del nombre y tipo SQL. |
| `quantity` | `int unsigned` | No | — | Cantidad de unidades del producto. |
| `unit_price` | `decimal(12,2)` | No | — | Precio unitario aplicado al producto en la operación. |
| `subtotal` | `decimal(12,2)` | Sí | — | Importe subtotal de la orden o línea. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |

### `tbd_products_categories`

Registros en el respaldo: **4,998**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `product_ID` | `int unsigned` | No | PK, FK | Producto asociado al registro. |
| `categories_ID` | `int unsigned` | No | PK, FK | Categoría asociada al producto. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | Fecha y hora de la última modificación. |

### `tbd_products_users_providers`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `user_ID` | `int` | No | PK, FK | Usuario propietario o asociado al registro. |
| `product_ID` | `int unsigned` | No | PK, FK | Producto asociado al registro. |
| `type_ownership` | `enum('Owner','Reseller','Distributor')` | Sí | — | Rol de propiedad o distribución del usuario sobre el producto. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `available_date` | `datetime` | No | — | Fecha desde la que el producto está disponible por ese proveedor. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | Fecha y hora de la última modificación. |

### `tbd_user_payment_methods`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `ID` | `bigint unsigned` | No | PK | Identificador único del registro. |
| `user_ID` | `int` | No | FK | Usuario propietario o asociado al registro. |
| `payment_method_type_ID` | `int` | No | FK | Tipo de método de pago utilizado. |
| `provider` | `varchar(60)` | No | UK | Proveedor o procesador externo del método de pago. |
| `provider_method_ref` | `varchar(255)` | No | UK | Referencia del método en el sistema del proveedor de pagos. |
| `label` | `varchar(100)` | Sí | — | Nombre descriptivo del método guardado por el usuario. |
| `last_four` | `char(4)` | Sí | — | Últimos cuatro dígitos del medio de pago. |
| `is_default` | `tinyint(1)` | No | — | Indica si es la opción predeterminada. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | Sí | — | Fecha y hora de la última modificación. |

### `tbd_users_wishlist_products`

Registros en el respaldo: **0**

| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |
|---|---|---|---|---|
| `user_ID` | `int` | No | PK, FK | Usuario propietario o asociado al registro. |
| `product_ID` | `int unsigned` | No | PK, FK | Producto asociado al registro. |
| `status` | `bit(1)` | No | — | Indicador de vigencia o habilitación del registro. |
| `creation_date` | `datetime` | No | — | Fecha y hora de creación del registro. |
| `last_update` | `datetime` | No | — | Fecha y hora de la última modificación. |

## Relaciones y cardinalidades

Cada FK declarada en el respaldo produce una relación de muchos registros de origen hacia un registro referenciado (N:1). La participación del lado que contiene la FK es opcional si la columna admite `NULL`.

- **Declarada:** `tb_buyer_orders.seller_ID` → `tb_users.ID` (N:1).
- **Declarada:** `tb_carts.user_ID` → `tb_users.ID` (N:1).
- **Declarada:** `tb_people.user_ID` → `tb_users.ID` (N:1).
- **Declarada:** `tb_user_addresses.user_ID` → `tb_users.ID` (N:1).
- **Declarada:** `tbc_categories.sup_id_category` → `tbc_categories.ID` (N:1).
- **Declarada:** `tbd_address_components.address_ID` → `tb_user_addresses.ID` (N:1).
- **Declarada:** `tbd_address_components.address_ID, address_sup_ID` → `tbd_address_components.address_ID, ID` (N:1).
- **Declarada:** `tbd_carts_items.cart_ID` → `tb_carts.ID` (N:1).
- **Declarada:** `tbd_carts_items.provider_ID` → `tbd_products_users_providers.user_ID` (N:1).
- **Declarada:** `tbd_carts_items.product_ID` → `tbd_products_users_providers.product_ID` (N:1).
- **Declarada:** `tbd_order_items.seller_order_ID` → `tb_buyer_orders.ID` (N:1).
- **Declarada:** `tbd_order_items.product_ID` → `tbd_products_users_providers.product_ID` (N:1).
- **Declarada:** `tbd_order_items.provider_ID` → `tbd_products_users_providers.user_ID` (N:1).
- **Declarada:** `tbd_products_categories.categories_ID` → `tbc_categories.ID` (N:1).
- **Declarada:** `tbd_products_categories.product_ID` → `tb_products.ID` (N:1).
- **Declarada:** `tbd_products_users_providers.product_ID` → `tb_products.ID` (N:1).
- **Declarada:** `tbd_products_users_providers.user_ID` → `tb_users.ID` (N:1).
- **Declarada:** `tbd_user_payment_methods.user_ID` → `tb_users.ID` (N:1).
- **Declarada:** `tbd_user_payment_methods.payment_method_type_ID` → `tbc_payment_methods_types.ID` (N:1).
- **Declarada:** `tbd_users_wishlist_products.product_ID` → `tb_products.ID` (N:1).
- **Declarada:** `tbd_users_wishlist_products.user_ID` → `tb_users.ID` (N:1).
- **Inferida (no es FK física):** `tb_logs.product_id` → `tb_products.ID` (N:1).
