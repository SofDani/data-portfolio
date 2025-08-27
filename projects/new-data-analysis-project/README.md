Problem
Many small shops & teams store data in CSVs but need normalized data for reporting or BI tools.

Solution
I implemented a small ETL pipeline (CSV → SQLite) that:
- Loads raw CSV into staging tables
- Normalizes to `orders` and `order_items`
- Calculates `line_total` and creates reporting tables
- Generates CSV reports: `monthly_revenue.csv` and `top_products.csv`

Deliverables
- `data.db` (SQLite file)
- `monthly_revenue.csv`, `top_products.csv`
- SQL queries file (`queries/reports.sql`) for rerunnable reports
- README with how-to and extension notes

Why this helps
- Lightweight, portable ETL suitable for automated runs
- Easy to extend to PostgreSQL/BigQuery later
- Good for small budgets (no DB server needed)

Repo / Demo
- GitHub: https://github.com/<SofDani>/data-portfolio/projects/sql-etl