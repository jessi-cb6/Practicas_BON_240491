USE `db_test_7b`;

-- Tablas que no están en el respaldo base.
CREATE TABLE IF NOT EXISTS `tb_orders` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `buyer_ID` int NOT NULL,
  `shipping_address_ID` bigint unsigned DEFAULT NULL,
  `subtotal` decimal(12,2) NOT NULL DEFAULT 0.00,
  `shipping_cost` decimal(12,2) NOT NULL DEFAULT 0.00,
  `order_status` enum('Pending','Paid','Processing','Shipped','Delivered','Canceled','Returned') NOT NULL DEFAULT 'Pending',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), KEY `idx_orders_buyer_created` (`buyer_ID`,`created_at`), KEY `idx_orders_address` (`shipping_address_ID`),
  CONSTRAINT `fk_orders_buyer` FOREIGN KEY (`buyer_ID`) REFERENCES `tb_users` (`ID`),
  CONSTRAINT `fk_orders_address` FOREIGN KEY (`shipping_address_ID`) REFERENCES `tb_user_addresses` (`ID`),
  CONSTRAINT `chk_orders_amounts` CHECK (`subtotal` >= 0 AND `shipping_cost` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_payment_methods` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(40) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), UNIQUE KEY `uk_payment_methods_code` (`code`), KEY `idx_payment_methods_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_payments` (
  `ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_ID` int unsigned NOT NULL,
  `payment_method_ID` int unsigned DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `currency` char(3) NOT NULL DEFAULT 'MXN',
  `payment_status` enum('Pending','Authorized','Paid','Failed','PartiallyRefunded','Refunded') NOT NULL DEFAULT 'Pending',
  `paid_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), KEY `idx_payments_order` (`order_ID`), KEY `idx_payments_method` (`payment_method_ID`), KEY `idx_payments_status_created` (`payment_status`,`created_at`),
  CONSTRAINT `fk_payments_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`),
  CONSTRAINT `fk_payments_method` FOREIGN KEY (`payment_method_ID`) REFERENCES `tb_payment_methods` (`ID`),
  CONSTRAINT `chk_payments_amount` CHECK (`amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_payment_transaction` (
  `ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `payment_ID` bigint unsigned NOT NULL,
  `transaction_ref` varchar(150) NOT NULL,
  `transaction_type` enum('Authorize','Capture','Void','Charge','Refund') NOT NULL,
  `transaction_status` enum('Pending','Succeeded','Failed') NOT NULL DEFAULT 'Pending',
  `amount` decimal(12,2) NOT NULL,
  `gateway` varchar(80) DEFAULT NULL,
  `response_code` varchar(80) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), UNIQUE KEY `uk_payment_transaction_ref` (`transaction_ref`), KEY `idx_payment_transaction_payment_date` (`payment_ID`,`created_at`),
  CONSTRAINT `fk_payment_transaction_payment` FOREIGN KEY (`payment_ID`) REFERENCES `tb_payments` (`ID`),
  CONSTRAINT `chk_payment_transaction_amount` CHECK (`amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_order_cancellations` (
  `ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_ID` int unsigned NOT NULL,
  `requested_by` int NOT NULL,
  `reason` varchar(500) NOT NULL,
  `cancellation_status` enum('Requested','Approved','Rejected','Completed') NOT NULL DEFAULT 'Requested',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), KEY `idx_cancellations_order` (`order_ID`), KEY `idx_cancellations_user` (`requested_by`),
  CONSTRAINT `fk_cancellations_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`),
  CONSTRAINT `fk_cancellations_user` FOREIGN KEY (`requested_by`) REFERENCES `tb_users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_shipments` (
  `ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_ID` int unsigned NOT NULL,
  `carrier` varchar(100) DEFAULT NULL,
  `tracking_number` varchar(150) DEFAULT NULL,
  `shipment_status` enum('Pending','Ready','InTransit','Delivered','Lost','Returned') NOT NULL DEFAULT 'Pending',
  `shipped_at` datetime DEFAULT NULL,
  `delivered_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), UNIQUE KEY `uk_shipments_tracking` (`tracking_number`), KEY `idx_shipments_order` (`order_ID`), KEY `idx_shipments_status` (`shipment_status`),
  CONSTRAINT `fk_shipments_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_returns` (
  `ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_ID` int unsigned NOT NULL,
  `requested_by` int NOT NULL,
  `return_status` enum('Requested','Approved','Rejected','InTransit','Received','Completed') NOT NULL DEFAULT 'Requested',
  `reason` varchar(500) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), KEY `idx_returns_order` (`order_ID`), KEY `idx_returns_user` (`requested_by`), KEY `idx_returns_status` (`return_status`),
  CONSTRAINT `fk_returns_order` FOREIGN KEY (`order_ID`) REFERENCES `tb_orders` (`ID`),
  CONSTRAINT `fk_returns_user` FOREIGN KEY (`requested_by`) REFERENCES `tb_users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tb_refunds` (
  `ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `payment_ID` bigint unsigned NOT NULL,
  `return_ID` bigint unsigned DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `refund_status` enum('Pending','Processing','Succeeded','Failed') NOT NULL DEFAULT 'Pending',
  `reason` varchar(500) DEFAULT NULL,
  `refunded_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`), KEY `idx_refunds_payment` (`payment_ID`), KEY `idx_refunds_return` (`return_ID`), KEY `idx_refunds_status` (`refund_status`),
  CONSTRAINT `fk_refunds_payment` FOREIGN KEY (`payment_ID`) REFERENCES `tb_payments` (`ID`),
  CONSTRAINT `fk_refunds_return` FOREIGN KEY (`return_ID`) REFERENCES `tb_returns` (`ID`),
  CONSTRAINT `chk_refunds_amount` CHECK (`amount` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tbd_cancellation_items` (
  `cancellation_ID` bigint unsigned NOT NULL,
  `order_item_ID` int unsigned NOT NULL,
  `quantity` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cancellation_ID`,`order_item_ID`), KEY `idx_cancellation_items_order_item` (`order_item_ID`),
  CONSTRAINT `fk_cancellation_items_cancellation` FOREIGN KEY (`cancellation_ID`) REFERENCES `tb_order_cancellations` (`ID`),
  CONSTRAINT `fk_cancellation_items_order_item` FOREIGN KEY (`order_item_ID`) REFERENCES `tbd_order_items` (`ID`),
  CONSTRAINT `chk_cancellation_items_quantity` CHECK (`quantity` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tbd_cart_items` (
  `cart_ID` int unsigned NOT NULL,
  `provider_ID` int NOT NULL,
  `product_ID` int unsigned NOT NULL,
  `quantity` int unsigned NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cart_ID`,`provider_ID`,`product_ID`), KEY `idx_cart_items_provider_product` (`provider_ID`,`product_ID`),
  CONSTRAINT `fk_cart_items_cart` FOREIGN KEY (`cart_ID`) REFERENCES `tb_carts` (`ID`),
  CONSTRAINT `fk_cart_items_provider_product` FOREIGN KEY (`provider_ID`,`product_ID`) REFERENCES `tbd_products_users_providers` (`user_ID`,`product_ID`),
  CONSTRAINT `chk_cart_items_quantity` CHECK (`quantity` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `tbd_return_items` (
  `return_ID` bigint unsigned NOT NULL,
  `order_item_ID` int unsigned NOT NULL,
  `quantity` int unsigned NOT NULL,
  `condition_note` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`return_ID`,`order_item_ID`), KEY `idx_return_items_order_item` (`order_item_ID`),
  CONSTRAINT `fk_return_items_return` FOREIGN KEY (`return_ID`) REFERENCES `tb_returns` (`ID`),
  CONSTRAINT `fk_return_items_order_item` FOREIGN KEY (`order_item_ID`) REFERENCES `tbd_order_items` (`ID`),
  CONSTRAINT `chk_return_items_quantity` CHECK (`quantity` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Auditoría JSON de las nuevas tablas. Los triggers existentes del respaldo se conservan.
DELIMITER //
CREATE TRIGGER `trg_tb_orders_insert` AFTER INSERT ON `tb_orders` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_orders','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'buyer_ID', NEW.`buyer_ID`, 'shipping_address_ID', NEW.`shipping_address_ID`, 'subtotal', NEW.`subtotal`, 'shipping_cost', NEW.`shipping_cost`, 'order_status', NEW.`order_status`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_orders_update` AFTER UPDATE ON `tb_orders` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_orders','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'buyer_ID', OLD.`buyer_ID`, 'shipping_address_ID', OLD.`shipping_address_ID`, 'subtotal', OLD.`subtotal`, 'shipping_cost', OLD.`shipping_cost`, 'order_status', OLD.`order_status`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'buyer_ID', NEW.`buyer_ID`, 'shipping_address_ID', NEW.`shipping_address_ID`, 'subtotal', NEW.`subtotal`, 'shipping_cost', NEW.`shipping_cost`, 'order_status', NEW.`order_status`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_orders_delete` AFTER DELETE ON `tb_orders` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_orders','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'buyer_ID', OLD.`buyer_ID`, 'shipping_address_ID', OLD.`shipping_address_ID`, 'subtotal', OLD.`subtotal`, 'shipping_cost', OLD.`shipping_cost`, 'order_status', OLD.`order_status`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_payment_methods_insert` AFTER INSERT ON `tb_payment_methods` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payment_methods','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'code', NEW.`code`, 'name', NEW.`name`, 'description', NEW.`description`, 'is_active', NEW.`is_active`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_payment_methods_update` AFTER UPDATE ON `tb_payment_methods` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payment_methods','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'code', OLD.`code`, 'name', OLD.`name`, 'description', OLD.`description`, 'is_active', OLD.`is_active`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'code', NEW.`code`, 'name', NEW.`name`, 'description', NEW.`description`, 'is_active', NEW.`is_active`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_payment_methods_delete` AFTER DELETE ON `tb_payment_methods` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payment_methods','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'code', OLD.`code`, 'name', OLD.`name`, 'description', OLD.`description`, 'is_active', OLD.`is_active`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_payments_insert` AFTER INSERT ON `tb_payments` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payments','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'payment_method_ID', NEW.`payment_method_ID`, 'amount', NEW.`amount`, 'currency', NEW.`currency`, 'payment_status', NEW.`payment_status`, 'paid_at', NEW.`paid_at`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_payments_update` AFTER UPDATE ON `tb_payments` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payments','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'payment_method_ID', OLD.`payment_method_ID`, 'amount', OLD.`amount`, 'currency', OLD.`currency`, 'payment_status', OLD.`payment_status`, 'paid_at', OLD.`paid_at`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'payment_method_ID', NEW.`payment_method_ID`, 'amount', NEW.`amount`, 'currency', NEW.`currency`, 'payment_status', NEW.`payment_status`, 'paid_at', NEW.`paid_at`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_payments_delete` AFTER DELETE ON `tb_payments` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payments','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'payment_method_ID', OLD.`payment_method_ID`, 'amount', OLD.`amount`, 'currency', OLD.`currency`, 'payment_status', OLD.`payment_status`, 'paid_at', OLD.`paid_at`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_payment_transaction_insert` AFTER INSERT ON `tb_payment_transaction` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payment_transaction','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'payment_ID', NEW.`payment_ID`, 'transaction_ref', NEW.`transaction_ref`, 'transaction_type', NEW.`transaction_type`, 'transaction_status', NEW.`transaction_status`, 'amount', NEW.`amount`, 'gateway', NEW.`gateway`, 'response_code', NEW.`response_code`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_payment_transaction_update` AFTER UPDATE ON `tb_payment_transaction` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payment_transaction','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'payment_ID', OLD.`payment_ID`, 'transaction_ref', OLD.`transaction_ref`, 'transaction_type', OLD.`transaction_type`, 'transaction_status', OLD.`transaction_status`, 'amount', OLD.`amount`, 'gateway', OLD.`gateway`, 'response_code', OLD.`response_code`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'payment_ID', NEW.`payment_ID`, 'transaction_ref', NEW.`transaction_ref`, 'transaction_type', NEW.`transaction_type`, 'transaction_status', NEW.`transaction_status`, 'amount', NEW.`amount`, 'gateway', NEW.`gateway`, 'response_code', NEW.`response_code`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_payment_transaction_delete` AFTER DELETE ON `tb_payment_transaction` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_payment_transaction','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'payment_ID', OLD.`payment_ID`, 'transaction_ref', OLD.`transaction_ref`, 'transaction_type', OLD.`transaction_type`, 'transaction_status', OLD.`transaction_status`, 'amount', OLD.`amount`, 'gateway', OLD.`gateway`, 'response_code', OLD.`response_code`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_order_cancellations_insert` AFTER INSERT ON `tb_order_cancellations` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_order_cancellations','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'requested_by', NEW.`requested_by`, 'reason', NEW.`reason`, 'cancellation_status', NEW.`cancellation_status`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_order_cancellations_update` AFTER UPDATE ON `tb_order_cancellations` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_order_cancellations','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'requested_by', OLD.`requested_by`, 'reason', OLD.`reason`, 'cancellation_status', OLD.`cancellation_status`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'requested_by', NEW.`requested_by`, 'reason', NEW.`reason`, 'cancellation_status', NEW.`cancellation_status`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_order_cancellations_delete` AFTER DELETE ON `tb_order_cancellations` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_order_cancellations','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'requested_by', OLD.`requested_by`, 'reason', OLD.`reason`, 'cancellation_status', OLD.`cancellation_status`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_shipments_insert` AFTER INSERT ON `tb_shipments` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_shipments','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'carrier', NEW.`carrier`, 'tracking_number', NEW.`tracking_number`, 'shipment_status', NEW.`shipment_status`, 'shipped_at', NEW.`shipped_at`, 'delivered_at', NEW.`delivered_at`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_shipments_update` AFTER UPDATE ON `tb_shipments` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_shipments','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'carrier', OLD.`carrier`, 'tracking_number', OLD.`tracking_number`, 'shipment_status', OLD.`shipment_status`, 'shipped_at', OLD.`shipped_at`, 'delivered_at', OLD.`delivered_at`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'carrier', NEW.`carrier`, 'tracking_number', NEW.`tracking_number`, 'shipment_status', NEW.`shipment_status`, 'shipped_at', NEW.`shipped_at`, 'delivered_at', NEW.`delivered_at`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_shipments_delete` AFTER DELETE ON `tb_shipments` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_shipments','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'carrier', OLD.`carrier`, 'tracking_number', OLD.`tracking_number`, 'shipment_status', OLD.`shipment_status`, 'shipped_at', OLD.`shipped_at`, 'delivered_at', OLD.`delivered_at`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_returns_insert` AFTER INSERT ON `tb_returns` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_returns','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'requested_by', NEW.`requested_by`, 'return_status', NEW.`return_status`, 'reason', NEW.`reason`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_returns_update` AFTER UPDATE ON `tb_returns` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_returns','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'requested_by', OLD.`requested_by`, 'return_status', OLD.`return_status`, 'reason', OLD.`reason`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'order_ID', NEW.`order_ID`, 'requested_by', NEW.`requested_by`, 'return_status', NEW.`return_status`, 'reason', NEW.`reason`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_returns_delete` AFTER DELETE ON `tb_returns` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_returns','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'order_ID', OLD.`order_ID`, 'requested_by', OLD.`requested_by`, 'return_status', OLD.`return_status`, 'reason', OLD.`reason`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tb_refunds_insert` AFTER INSERT ON `tb_refunds` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_refunds','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('ID', NEW.`ID`, 'payment_ID', NEW.`payment_ID`, 'return_ID', NEW.`return_ID`, 'amount', NEW.`amount`, 'refund_status', NEW.`refund_status`, 'reason', NEW.`reason`, 'refunded_at', NEW.`refunded_at`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_refunds_update` AFTER UPDATE ON `tb_refunds` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_refunds','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'payment_ID', OLD.`payment_ID`, 'return_ID', OLD.`return_ID`, 'amount', OLD.`amount`, 'refund_status', OLD.`refund_status`, 'reason', OLD.`reason`, 'refunded_at', OLD.`refunded_at`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('ID', NEW.`ID`, 'payment_ID', NEW.`payment_ID`, 'return_ID', NEW.`return_ID`, 'amount', NEW.`amount`, 'refund_status', NEW.`refund_status`, 'reason', NEW.`reason`, 'refunded_at', NEW.`refunded_at`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tb_refunds_delete` AFTER DELETE ON `tb_refunds` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tb_refunds','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('ID', OLD.`ID`, 'payment_ID', OLD.`payment_ID`, 'return_ID', OLD.`return_ID`, 'amount', OLD.`amount`, 'refund_status', OLD.`refund_status`, 'reason', OLD.`reason`, 'refunded_at', OLD.`refunded_at`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tbd_cancellation_items_insert` AFTER INSERT ON `tbd_cancellation_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_cancellation_items','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('cancellation_ID', NEW.`cancellation_ID`, 'order_item_ID', NEW.`order_item_ID`, 'quantity', NEW.`quantity`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tbd_cancellation_items_update` AFTER UPDATE ON `tbd_cancellation_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_cancellation_items','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('cancellation_ID', OLD.`cancellation_ID`, 'order_item_ID', OLD.`order_item_ID`, 'quantity', OLD.`quantity`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('cancellation_ID', NEW.`cancellation_ID`, 'order_item_ID', NEW.`order_item_ID`, 'quantity', NEW.`quantity`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tbd_cancellation_items_delete` AFTER DELETE ON `tbd_cancellation_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_cancellation_items','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('cancellation_ID', OLD.`cancellation_ID`, 'order_item_ID', OLD.`order_item_ID`, 'quantity', OLD.`quantity`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tbd_cart_items_insert` AFTER INSERT ON `tbd_cart_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_cart_items','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('cart_ID', NEW.`cart_ID`, 'provider_ID', NEW.`provider_ID`, 'product_ID', NEW.`product_ID`, 'quantity', NEW.`quantity`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tbd_cart_items_update` AFTER UPDATE ON `tbd_cart_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_cart_items','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('cart_ID', OLD.`cart_ID`, 'provider_ID', OLD.`provider_ID`, 'product_ID', OLD.`product_ID`, 'quantity', OLD.`quantity`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('cart_ID', NEW.`cart_ID`, 'provider_ID', NEW.`provider_ID`, 'product_ID', NEW.`product_ID`, 'quantity', NEW.`quantity`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tbd_cart_items_delete` AFTER DELETE ON `tbd_cart_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_cart_items','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('cart_ID', OLD.`cart_ID`, 'provider_ID', OLD.`provider_ID`, 'product_ID', OLD.`product_ID`, 'quantity', OLD.`quantity`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
CREATE TRIGGER `trg_tbd_return_items_insert` AFTER INSERT ON `tbd_return_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_return_items','Create',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', NULL, 'new', JSON_OBJECT('return_ID', NEW.`return_ID`, 'order_item_ID', NEW.`order_item_ID`, 'quantity', NEW.`quantity`, 'condition_note', NEW.`condition_note`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tbd_return_items_update` AFTER UPDATE ON `tbd_return_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_return_items','Update',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('return_ID', OLD.`return_ID`, 'order_item_ID', OLD.`order_item_ID`, 'quantity', OLD.`quantity`, 'condition_note', OLD.`condition_note`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', JSON_OBJECT('return_ID', NEW.`return_ID`, 'order_item_ID', NEW.`order_item_ID`, 'quantity', NEW.`quantity`, 'condition_note', NEW.`condition_note`, 'created_at', NEW.`created_at`, 'updated_at', NEW.`updated_at`)), b'1');
END//
CREATE TRIGGER `trg_tbd_return_items_delete` AFTER DELETE ON `tbd_return_items` FOR EACH ROW
BEGIN
  INSERT INTO `tb_logs` (`table_name`,`table_operation`,`db_user`,`operation_date`,`operation_description`,`operation_status`)
  VALUES ('tbd_return_items','Delete',USER(),CURRENT_TIMESTAMP,
          JSON_OBJECT('old', JSON_OBJECT('return_ID', OLD.`return_ID`, 'order_item_ID', OLD.`order_item_ID`, 'quantity', OLD.`quantity`, 'condition_note', OLD.`condition_note`, 'created_at', OLD.`created_at`, 'updated_at', OLD.`updated_at`), 'new', NULL), b'1');
END//
DELIMITER ;

-- Vistas de trazabilidad: 25 para las 25 tablas del esquema objetivo.
-- Las cinco vistas que ya existen en el respaldo se conservan sin recrearlas:
-- vw_trazabilidad_categorias, vw_trazabilidad_categorizacion_productos,
-- vw_trazabilidad_people, vw_trazabilidad_productos y vw_trazabilidad_usuarios.
-- También se conserva vw_total_products_by_category, que ya viene en el respaldo.
CREATE VIEW `vw_trazabilidad_carts` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_carts';

CREATE VIEW `vw_trazabilidad_order_cancellations` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_order_cancellations';

CREATE VIEW `vw_trazabilidad_orders` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_orders';

CREATE VIEW `vw_trazabilidad_payment_methods` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_payment_methods';

CREATE VIEW `vw_trazabilidad_payment_transaction` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_payment_transaction';

CREATE VIEW `vw_trazabilidad_payments` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_payments';

CREATE VIEW `vw_trazabilidad_refunds` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_refunds';

CREATE VIEW `vw_trazabilidad_returns` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_returns';

CREATE VIEW `vw_trazabilidad_shipments` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_shipments';

CREATE VIEW `vw_trazabilidad_user_addresses` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tb_user_addresses';

CREATE VIEW `vw_trazabilidad_payment_methods_types` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbc_payment_methods_types';

CREATE VIEW `vw_trazabilidad_address_components` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_address_components';

CREATE VIEW `vw_trazabilidad_cancellation_items` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_cancellation_items';

CREATE VIEW `vw_trazabilidad_cart_items` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_cart_items';

CREATE VIEW `vw_trazabilidad_order_items` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_order_items';

CREATE VIEW `vw_trazabilidad_products_users_providers` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_products_users_providers';

CREATE VIEW `vw_trazabilidad_return_items` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_return_items';

CREATE VIEW `vw_trazabilidad_user_payment_methods` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_user_payment_methods';

CREATE VIEW `vw_trazabilidad_users_wishlist_products` AS
SELECT l.ID AS log_id,l.table_name,l.table_operation AS operation,l.db_user,
       SUBSTRING_INDEX(l.db_user,'@',1) AS username,l.operation_description,
       l.operation_date,l.operation_status,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.old') END AS old_values,
       CASE WHEN JSON_VALID(l.operation_description) THEN JSON_EXTRACT(l.operation_description,'$.new') END AS new_values
FROM tb_logs l
WHERE l.table_name='tbd_users_wishlist_products';