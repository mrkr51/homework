SET search_path TO public;

DROP VIEW IF EXISTS top_5_profitable_cakes CASCADE;
DROP TABLE IF EXISTS recipe_ingredients CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS recipes CASCADE;
DROP TABLE IF EXISTS ingredients CASCADE;
DROP TABLE IF EXISTS clients CASCADE;
DROP FUNCTION IF EXISTS get_order_ingredients(INT);

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(10),
    price_per_unit DECIMAL(10, 2) NOT NULL
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_selling_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER REFERENCES recipes(id),
    ingredient_id INTEGER REFERENCES ingredients(id),
    quantity DECIMAL(10, 3) NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    recipe_id INTEGER REFERENCES recipes(id),
    order_date DATE DEFAULT CURRENT_DATE,
    total_price DECIMAL(10, 2),
    status VARCHAR(50)
);

CREATE VIEW top_5_profitable_cakes AS
WITH cake_costs AS (
    SELECT
        r.id AS recipe_id,
        r.name,
        SUM(ri.quantity * i.price_per_unit) AS cost_price
    FROM recipes r
    JOIN recipe_ingredients ri ON r.id = ri.recipe_id
    JOIN ingredients i ON ri.ingredient_id = i.id
    GROUP BY r.id, r.name
)
SELECT
    cc.name AS cake_name,
    SUM(o.total_price - cc.cost_price) AS total_profit
FROM orders o
JOIN cake_costs cc ON o.recipe_id = cc.recipe_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY cc.name
ORDER BY total_profit DESC
LIMIT 5;

CREATE OR REPLACE FUNCTION get_order_ingredients(p_order_id INT)
RETURNS TABLE(ingredient_name VARCHAR, amount DECIMAL, cost DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT i.name, ri.quantity, (ri.quantity * i.price_per_unit)
    FROM orders o
    JOIN recipe_ingredients ri ON o.recipe_id = ri.recipe_id
    JOIN ingredients i ON ri.ingredient_id = i.id
    WHERE o.id = p_order_id;
END;
$$ LANGUAGE plpgsql;

INSERT INTO ingredients (name, unit, price_per_unit) VALUES
('Мука', 'кг', 60), ('Сахар', 'кг', 80), ('Сливки', 'л', 400), ('Клубника', 'кг', 800);

INSERT INTO recipes (name, base_selling_price) VALUES
('Клубничный бархат', 2500), ('Медовик', 1800);

INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES
(1, 1, 0.5), (1, 2, 0.2), (1, 4, 0.3), (2, 1, 0.6), (2, 2, 0.3);

INSERT INTO clients (full_name, phone) VALUES ('Иван Иванов', '89991234567');

INSERT INTO orders (client_id, recipe_id, total_price, status) VALUES
(1, 1, 2800, 'delivered'), (1, 2, 1800, 'delivered');