-- Recorta db_test_7b a 7,008 productos y reconstruye 15,000 relaciones
-- producto-categoria distribuidas por hojas y sus ancestros.
-- Origen de referencia: respaldos/practica3_terminada2.sql
-- Selección determinista: conserva los 7,008 productos con menor ID.
-- Ejecutar una sola vez en MySQL 8.0; si se vuelve a ejecutar, elegirá de nuevo
-- los 7,008 IDs menores y reconstruirá las mismas 15,000 asociaciones.

USE db_test_7b;

DELIMITER //
DROP PROCEDURE IF EXISTS sp_codex_recategorizacion_productos_7008//
CREATE PROCEDURE sp_codex_recategorizacion_productos_7008()
BEGIN
    DECLARE v_products_before INT DEFAULT 0;
    DECLARE v_keep_count INT DEFAULT 0;
    DECLARE v_keep_max INT UNSIGNED DEFAULT 0;
    DECLARE v_leaf_count INT DEFAULT 0;
    DECLARE v_link_count INT DEFAULT 0;
    DECLARE v_uncovered_count INT DEFAULT 0;
    DECLARE v_product_refs INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    SELECT COUNT(*) INTO v_products_before FROM tb_products;
    IF v_products_before < 7008 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se requieren al menos 7008 productos; no se modificaron datos.';
    END IF;

    SELECT COUNT(*) INTO v_leaf_count
    FROM tbc_categories AS c
    LEFT JOIN tbc_categories AS child ON child.sup_id_category = c.ID
    WHERE child.ID IS NULL;
    IF v_leaf_count = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No hay categorías hoja; no se modificaron datos.';
    END IF;

    DROP TEMPORARY TABLE IF EXISTS tmp_codex_keep_products;
    DROP TEMPORARY TABLE IF EXISTS tmp_codex_product_leaf;
    DROP TEMPORARY TABLE IF EXISTS tmp_codex_category_links;

    CREATE TEMPORARY TABLE tmp_codex_keep_products (
        product_ID INT UNSIGNED NOT NULL PRIMARY KEY
    ) ENGINE=InnoDB;

    INSERT INTO tmp_codex_keep_products (product_ID)
    SELECT ID FROM tb_products ORDER BY ID LIMIT 7008;
    SELECT COUNT(*) INTO v_keep_count FROM tmp_codex_keep_products;
    IF v_keep_count <> 7008 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La selección no produjo exactamente 7008 productos; no se modificaron datos.';
    END IF;
    SELECT MAX(product_ID) INTO v_keep_max FROM tmp_codex_keep_products;

    -- Evita que el recorte borre productos referenciados por proveedores o deseos.
    SELECT COUNT(*) INTO v_product_refs
    FROM tbd_products_users_providers AS p
    LEFT JOIN tmp_codex_keep_products AS k ON k.product_ID = p.product_ID
    WHERE k.product_ID IS NULL;
    IF v_product_refs > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Hay productos por recortar usados por proveedores; se abortó sin borrar datos.';
    END IF;

    SELECT COUNT(*) INTO v_product_refs
    FROM tbd_users_wishlist_products AS w
    LEFT JOIN tmp_codex_keep_products AS k ON k.product_ID = w.product_ID
    WHERE k.product_ID IS NULL;
    IF v_product_refs > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Hay productos por recortar en listas de deseos; se abortó sin borrar datos.';
    END IF;

    CREATE TEMPORARY TABLE tmp_codex_product_leaf (
        product_ID INT UNSIGNED NOT NULL PRIMARY KEY,
        leaf_category_ID INT UNSIGNED NOT NULL
    ) ENGINE=InnoDB;

    -- Reparte los productos de forma pareja entre todas las hojas por ID.
    INSERT INTO tmp_codex_product_leaf (product_ID, leaf_category_ID)
    WITH ranked_leaves AS (
        SELECT c.ID, ROW_NUMBER() OVER (ORDER BY c.ID) AS leaf_no
        FROM tbc_categories AS c
        LEFT JOIN tbc_categories AS child ON child.sup_id_category = c.ID
        WHERE child.ID IS NULL
    ),
    ranked_products AS (
        SELECT product_ID, ROW_NUMBER() OVER (ORDER BY product_ID) AS product_no
        FROM tmp_codex_keep_products
    )
    SELECT p.product_ID, l.ID
    FROM ranked_products AS p
    JOIN ranked_leaves AS l
        ON l.leaf_no = MOD(p.product_no - 1, v_leaf_count) + 1;

    CREATE TEMPORARY TABLE tmp_codex_category_links (
        product_ID INT UNSIGNED NOT NULL,
        categories_ID INT UNSIGNED NOT NULL,
        hierarchy_depth INT UNSIGNED NOT NULL,
        PRIMARY KEY (product_ID, categories_ID)
    ) ENGINE=InnoDB;

    -- Cada producto hereda vínculos de su categoría hoja hacia padres y ancestros.
    -- Se reserva una primera asociación para cada categoría y se completa hasta 15,000.
    INSERT INTO tmp_codex_category_links (product_ID, categories_ID, hierarchy_depth)
    WITH RECURSIVE category_paths AS (
        SELECT product_ID, leaf_category_ID AS categories_ID, 0 AS hierarchy_depth
        FROM tmp_codex_product_leaf
        UNION ALL
        SELECT path.product_ID, current_category.sup_id_category, path.hierarchy_depth + 1
        FROM category_paths AS path
        JOIN tbc_categories AS current_category ON current_category.ID = path.categories_ID
        WHERE current_category.sup_id_category IS NOT NULL
          AND path.hierarchy_depth < 99
    ),
    category_rank AS (
        SELECT product_ID, categories_ID, hierarchy_depth,
               ROW_NUMBER() OVER (PARTITION BY categories_ID ORDER BY hierarchy_depth, product_ID) AS category_pick
        FROM category_paths
    ),
    ranked_links AS (
        SELECT product_ID, categories_ID, hierarchy_depth,
               ROW_NUMBER() OVER (
                   ORDER BY (category_pick <> 1), hierarchy_depth, category_pick, categories_ID, product_ID
               ) AS link_no
        FROM category_rank
    )
    SELECT product_ID, categories_ID, hierarchy_depth
    FROM ranked_links
    WHERE link_no <= 15000;

    SELECT COUNT(*) INTO v_link_count FROM tmp_codex_category_links;
    IF v_link_count <> 15000 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La jerarquía no permite 15000 asociaciones; se abortó sin borrar datos.';
    END IF;

    SELECT COUNT(*) INTO v_uncovered_count
    FROM tbc_categories AS c
    LEFT JOIN (
        SELECT DISTINCT categories_ID FROM tmp_codex_category_links
    ) AS used_categories ON used_categories.categories_ID = c.ID
    WHERE used_categories.categories_ID IS NULL;
    IF v_uncovered_count > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Quedaron categorías sin cobertura en la selección; se abortó sin borrar datos.';
    END IF;

    START TRANSACTION;

    -- Reemplaza las asociaciones anteriores y elimina solo los productos no retenidos.
    DELETE FROM tbd_products_categories
    WHERE product_ID BETWEEN 1 AND 4294967295;
    DELETE FROM tb_products
    WHERE ID > v_keep_max;

    INSERT INTO tbd_products_categories
        (product_ID, categories_ID, status, creation_date, last_update)
    SELECT product_ID, categories_ID, b'1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
    FROM tmp_codex_category_links;

    COMMIT;

    SELECT
        (SELECT COUNT(*) FROM tb_products) AS productos,
        (SELECT COUNT(*) FROM tbd_products_categories) AS asociaciones_producto_categoria,
        (SELECT COUNT(DISTINCT product_ID) FROM tbd_products_categories) AS productos_categorizados,
        (SELECT COUNT(*) FROM tbc_categories c
         LEFT JOIN tbd_products_categories pc ON pc.categories_ID = c.ID
         WHERE pc.product_ID IS NULL) AS categorias_sin_asociaciones;

    SELECT c.ID, c.name, c.sup_id_category AS categoria_padre, COUNT(pc.product_ID) AS productos_asociados
    FROM tbc_categories AS c
    LEFT JOIN tbd_products_categories AS pc ON pc.categories_ID = c.ID
    GROUP BY c.ID, c.name, c.sup_id_category
    ORDER BY c.ID;
END//
DELIMITER ;

CALL sp_codex_recategorizacion_productos_7008();
DROP PROCEDURE IF EXISTS sp_codex_recategorizacion_productos_7008;
