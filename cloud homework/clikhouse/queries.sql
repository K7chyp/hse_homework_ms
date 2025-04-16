SELECT 
    payment_status,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_sum,
    AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY payment_status;

SELECT 
    o.order_id,
    SUM(oi.quantity) AS total_items,
    SUM(oi.price * oi.quantity) AS total_revenue,
    AVG(oi.price) AS avg_product_price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;

SELECT 
    order_date,
    COUNT(*) AS daily_orders,
    SUM(total_amount) AS daily_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;

SELECT 
    user_id,
    SUM(total_amount) AS total_spent
FROM orders
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 10;

SELECT 
    user_id,
    COUNT(*) AS order_count
FROM orders
GROUP BY user_id
ORDER BY order_count DESC
LIMIT 10;