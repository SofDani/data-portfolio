# -*- coding: utf-8 -*-
"""
Process Shopify export: clean and aggregate for dashboard (pandas).
Run: python process_shopify.py
"""
# -*- coding: utf-8 -*-
"""
Process Shopify export: clean and aggregate for dashboard (pandas).
Run: python process_shopify.py
"""
import pandas as pd
from pathlib import Path

SRC = Path(__file__).parent  # projects/shopify-dashboard
IN = SRC / "input_shopify_orders.csv"
OUT_DIR = SRC / "output"
OUT_DIR.mkdir(exist_ok=True)

def load_and_clean(path):
    df = pd.read_csv(path, low_memory=False)
    # Basic cleaning
    df.columns = df.columns.str.strip()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['customer_id'] = df['customer_id'].fillna('guest')
    df['product_name'] = df['product_name'].astype(str).str.strip()
    df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce').fillna(0.0)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)
    # Remove exact duplicates
    df = df.drop_duplicates()
    return df

def build_outputs(df):
    # cleaned CSV for upload to Google Sheets
    cleaned_path = OUT_DIR / "cleaned_sales.csv"
    df.to_csv(cleaned_path, index=False)

    # summary metrics for fast dashboard cards
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    summary = {}
    summary['total_revenue'] = df['total_price'].sum()
    summary['orders_count'] = df['order_id'].nunique()
    summary['avg_order_value'] = summary['total_revenue'] / max(1, summary['orders_count'])
    by_day = df.groupby(df['order_date'].dt.date).agg({'total_price':'sum','order_id':'nunique'}).reset_index()
    top_products = df.groupby('product_name').agg({'quantity':'sum','total_price':'sum'}).reset_index().sort_values('total_price', ascending=False).head(10)
    # Save small reports
    (OUT_DIR / "summary_metrics.csv").write_text(
        f"metric,value\n"
        f"total_revenue,{summary['total_revenue']}\n"
        f"orders_count,{summary['orders_count']}\n"
        f"avg_order_value,{summary['avg_order_value']}\n"
    )
    top_products.to_csv(OUT_DIR / "top_products.csv", index=False)
    by_day.to_csv(OUT_DIR / "revenue_by_day.csv", index=False)
    print("Outputs written to:", OUT_DIR)
    return cleaned_path

if __name__ == "__main__":
    df = load_and_clean(IN)
    build_outputs(df)



