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

## Как да включите в портфолио
- Кратко описание: „ETL pipeline (CSV → SQLite) with normalization and reporting“
- Включете `queries/reports.sql` и кратки снимки/CSV резултати.