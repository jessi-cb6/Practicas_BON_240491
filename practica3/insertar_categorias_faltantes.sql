-- Genera 100 productos por cada categoría que no tenga productos asociados:
-- 50 activos y 50 inactivos. Compatible con MySQL 8.0.
-- Debe ejecutarse en la base db_test_7b después de cargar el respaldo.
-- Usa el patrón de precio y stock de productos_extra_2000.sql y un prefijo SKU nuevo.

USE db_test_7b;

DROP TEMPORARY TABLE IF EXISTS tmp_categorias_sin_productos;

CREATE TEMPORARY TABLE tmp_categorias_sin_productos (
    category_ID INT UNSIGNED NOT NULL PRIMARY KEY,
    category_name VARCHAR(120) NOT NULL
) ENGINE=InnoDB;

INSERT INTO tmp_categorias_sin_productos (category_ID, category_name)
SELECT c.ID, c.name
FROM tbc_categories AS c
LEFT JOIN tbd_products_categories AS pc
    ON pc.categories_ID = c.ID
WHERE pc.product_ID IS NULL;

SET @old_cte_max_recursion_depth = @@SESSION.cte_max_recursion_depth;
SET SESSION cte_max_recursion_depth = 2100;

START TRANSACTION;

-- SKU: PRACTICA3-FULL-<category_ID>-<consecutivo por categoría>
-- El consecutivo 001-050 queda activo; 051-100 queda inactivo.
INSERT IGNORE INTO tb_products
    (SKU, name, description, current_price, current_stock, status, creation_date, last_update)
WITH RECURSIVE seq (n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 100
)
SELECT
    CONCAT('PRACTICA3-FULL-', LPAD(c.category_ID, 3, '0'), '-', LPAD(seq.n, 3, '0')),
    CONCAT(LEFT(c.category_name, 180), ' practica ', LPAD(seq.n, 3, '0')),
    CONCAT('Producto de practica para la categoria ', c.category_name, '.'),
    ROUND(100 + MOD(seq.n * 137, 990000) / 100, 2),
    1 + MOD(seq.n * 17, 100),
    IF(seq.n <= 50, b'1', b'0'),
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM tmp_categorias_sin_productos AS c
CROSS JOIN seq;

-- Asocia cada producto recién generado con la categoría que figura en su SKU.
INSERT IGNORE INTO tbd_products_categories
    (product_ID, categories_ID, status, creation_date, last_update)
WITH RECURSIVE seq (n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 100
)
SELECT
    p.ID,
    c.category_ID,
    b'1',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM tmp_categorias_sin_productos AS c
CROSS JOIN seq
JOIN tb_products AS p
    ON p.SKU = CONCAT('PRACTICA3-FULL-', LPAD(c.category_ID, 3, '0'), '-', LPAD(seq.n, 3, '0'));

COMMIT;

SET SESSION cte_max_recursion_depth = @old_cte_max_recursion_depth;

-- Resumen de productos y asociaciones creados por este prefijo.
SELECT
    COUNT(*) AS productos_generados,
    SUM(status = b'1') AS productos_activos,
    SUM(status = b'0') AS productos_inactivos
FROM tb_products
WHERE SKU LIKE 'PRACTICA3-FULL-%';

SELECT COUNT(*) AS asociaciones_generadas
FROM tbd_products_categories AS pc
JOIN tb_products AS p ON p.ID = pc.product_ID
WHERE p.SKU LIKE 'PRACTICA3-FULL-%';

-- Debe devolver cero filas: categorías sin productos vinculados.
SELECT c.ID AS category_ID, c.name AS category_name
FROM tbc_categories AS c
LEFT JOIN tbd_products_categories AS pc ON pc.categories_ID = c.ID
WHERE pc.product_ID IS NULL;

DROP TEMPORARY TABLE IF EXISTS tmp_categorias_sin_productos;

-- Verificación opcional si la vista está instalada en la base:
-- SELECT *
-- FROM db_test_7b.vw_total_products_by_category
-- WHERE total_products = 0;
