# SQL ETL demo (SQLite)

## Какво показва проектът
- Как да импортираш CSV в SQLite (staging tables)
- Как да нормализираш/трансформираш (orders, order_items)
- Как да изкараш стандартни отчети (monthly revenue, top products)
- Всичко е offline — генерира CSV репорти за dashboard

## Как да стартирате
1. Отидете в `projects/sql-etl`.
2. Инсталирайте pandas: `pip install pandas`.
3. Стартирайте: `python scripts/load_and_transform.py`.
4. Резултати: `data.db` (SQLite file), `monthly_revenue.csv`, `top_products.csv`.





-- sample queries you can run in sqlite3 or DB browser
-- 1) Monthly revenue
SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.line_total) as revenue
FROM orders o
JOIN order_items oi USING(order_id)
GROUP BY month;

-- 2) Top products
SELECT p.product_name, SUM(oi.line_total) as revenue
FROM order_items oi
LEFT JOIN dim_products p ON p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY revenue DESC;