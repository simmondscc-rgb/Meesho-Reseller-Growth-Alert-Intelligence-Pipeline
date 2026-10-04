-- Part 1: SQL Business Query Engine
-- Run against data/meesho_reseller.db

-- Query 1: Monthly revenue by category
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
    category;

-- Query 2: Region-wise total revenue and order count
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

-- Query 3: Top resellers by total spend (> 50000), top 5
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Query 4a: Resellers who have never placed an order
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- Query 4b: Why COUNT(*) cannot detect the zero-match case.
-- For a reseller with no orders, the LEFT JOIN still produces ONE row with
-- every orders column NULL. COUNT(*) counts that row -> 1. COUNT(order_id)
-- counts only non-NULL values -> 0. So "COUNT(*) = 0" never fires for an
-- unmatched reseller; the correct test is COUNT(order_id) = 0.
SELECT
    r.reseller_id,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;

-- Query 5: AOV for June, Delivered orders only
SELECT
    ROUND(SUM(quantity * unit_price) * 1.0 / COUNT(*), 2) AS aov_june_delivered
FROM orders
WHERE month = 'June' AND status = 'Delivered';