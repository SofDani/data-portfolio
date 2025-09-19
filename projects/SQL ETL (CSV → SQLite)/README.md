# SQL ETL demo (SQLite)

## What the project shows
- How to import CSV into SQLite (staging tables)
- How to normalize/transform(orders, order_items)
- How to run standard reports(monthly revenue, top products)
- Everything is offline - generates CSV reports for dashboard

## How to start
1. Go to `projects/sql-etl`.
2. Install pandas: `pip install pandas`.
3. Start: `python scripts/load_and_transform.py`.
4. Results: `data.db` (SQLite file), `monthly_revenue.csv`, `top_products.csv`.





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