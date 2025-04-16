SELECT currency, SUM(amount) AS total_amount
FROM transactions_v2
WHERE currency IN ('USD', 'EUR', 'RUB')
GROUP BY currency;

SELECT
    is_fraud,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM transactions_v2
GROUP BY is_fraud;

SELECT
    transaction_date,
    COUNT(*) AS daily_transactions,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM transactions_v2
GROUP BY transaction_date;

SELECT
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions_v2
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY year, month;

SELECT
    t.transaction_id,
    COUNT(l.log_id) AS log_count,
    COLLECT_LIST(l.category) AS categories
FROM transactions_v2 t
LEFT JOIN logs_v2 l ON t.transaction_id = l.transaction_id
GROUP BY t.transaction_id
HAVING log_count > 1; 