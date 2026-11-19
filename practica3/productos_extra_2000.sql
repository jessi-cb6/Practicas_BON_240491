-- Agrega 2,000 productos de práctica y los vincula a categorías existentes.
-- Compatible con MySQL 8.0. Ejecutar después de cargar practica3_terminada.sql.
-- El archivo es reejecutable: SKU y relaciones repetidas se omiten.

SET @old_cte_max_recursion_depth = @@SESSION.cte_max_recursion_depth;
SET SESSION cte_max_recursion_depth = 2100;

START TRANSACTION;

INSERT IGNORE INTO tb_products
    (SKU, name, description, current_price, current_stock, status, creation_date, last_update)
WITH RECURSIVE seq (n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 2000
), category_options (slot, category_ID, category_name) AS (
    SELECT 0, 29, 'Bolsas y Mochilas' UNION ALL
    SELECT 1, 31, 'Relojes' UNION ALL
    SELECT 2, 37, 'Computacion' UNION ALL
    SELECT 3, 40, 'Video y TV' UNION ALL
    SELECT 4, 41, 'Laptops' UNION ALL
    SELECT 5, 42, 'Componentes de PC' UNION ALL
    SELECT 6, 43, 'Perifericos' UNION ALL
    SELECT 7, 46, 'Audifonos' UNION ALL
    SELECT 8, 47, 'Bocinas' UNION ALL
    SELECT 9, 52, 'Muebles' UNION ALL
    SELECT 10, 88, 'Oficina'
)
SELECT
    CONCAT('PRACTICA3-', LPAD(seq.n, 6, '0')),
    CONCAT(category_options.category_name, ' de practica ', LPAD(seq.n, 4, '0')),
    CONCAT('Producto generado para practica 3. Categoria: ', category_options.category_name, '.'),
    ROUND(100 + MOD(seq.n * 137, 990000) / 100, 2),
    1 + MOD(seq.n * 17, 100),
    b'1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM seq
JOIN category_options ON category_options.slot = MOD(seq.n - 1, 11);

INSERT IGNORE INTO tbd_products_categories
    (product_ID, categories_ID, status, creation_date, last_update)
WITH RECURSIVE seq (n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 2000
), category_options (slot, category_ID) AS (
    SELECT 0, 29 UNION ALL
    SELECT 1, 31 UNION ALL
    SELECT 2, 37 UNION ALL
    SELECT 3, 40 UNION ALL
    SELECT 4, 41 UNION ALL
    SELECT 5, 42 UNION ALL
    SELECT 6, 43 UNION ALL
    SELECT 7, 46 UNION ALL
    SELECT 8, 47 UNION ALL
    SELECT 9, 52 UNION ALL
    SELECT 10, 88
)
SELECT products.ID, category_options.category_ID, b'1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM seq
JOIN category_options ON category_options.slot = MOD(seq.n - 1, 11)
JOIN tb_products AS products
    ON products.SKU = CONCAT('PRACTICA3-', LPAD(seq.n, 6, '0'));

COMMIT;

SET SESSION cte_max_recursion_depth = @old_cte_max_recursion_depth;

-- Comprobacion de productos agregados por este archivo:
SELECT COUNT(*) AS productos_practica3
FROM tb_products
WHERE SKU LIKE 'PRACTICA3-%';

-- Comprobacion de sus asociaciones producto-categoria:
SELECT COUNT(*) AS asociaciones_practica3
FROM tbd_products_categories AS pc
JOIN tb_products AS p ON p.ID = pc.product_ID
WHERE p.SKU LIKE 'PRACTICA3-%';
