https://docs.google.com/spreadsheets/d/1CvRQIo8ZtxfViCzqGVM70-SZ5yVFpGOvIVrX5wc5wqY/edit?usp=sharing
https://lookerstudio.google.com/reporting/17022bb4-ef54-4392-83db-693bbc57fbf7

Problem
Shopify exports are useful but rarely ready for quick insights: inconsistent product names, guest customers, or missing fields make dashboarding slow.

Solution
I prepared a repeatable pipeline:
1. Clean Shopify orders export (normalize product names, fix currency/price types, handle guest customers)
2. Export cleaned data to Google Sheets (for easy sharing)
3. Build a Looker Studio dashboard with key KPIs:
   - Revenue trend (time series)
   - Top products by revenue
   - Average Order Value & Orders count
   - Simple filters (date range, channel)

Deliverables
- `cleaned_sales.csv` (upload-ready for Google Sheets)
- `summary_metrics.csv` & `top_products.csv`
- Link to Looker Studio dashboard (public view or with access)
- README with steps to refresh data (manual / schedule using Google Sheets)

Why this helps
- One-click dashboard refresh when new CSVs are uploaded
- Non-technical users can view insights in Looker Studio
- Low-cost setup, no paid tools required