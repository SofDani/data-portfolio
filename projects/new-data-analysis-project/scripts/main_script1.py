# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 06:47:47 2025

@author: PC
"""

# -*- coding: utf-8 -*-
"""
Simple ETL example: load CSVs into SQLite, normalize, produce reports.
Run: python load_and_transform.py
"""
import sqlite3
import pandas as pd
from pathlib import Path

# --- 1. DEFINE CORRECT PATHS ---
# This approach works both when running as a script and in interactive environments (Jupyter, Spyder)
try:
    # When running as a file (python main_script.py)
    SCRIPT_DIR = Path(__file__).parent
except NameError:
    # When running interactively
    SCRIPT_DIR = Path.cwd()

# Main project directory (one folder "up" from 'scripts')
PROJECT_ROOT = SCRIPT_DIR.parent

# Define paths for data, database, and reports
DB = PROJECT_ROOT / "data.db"
INPUT_DIR = PROJECT_ROOT / "sample_input"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Ensure the reports folder exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Main project directory: {PROJECT_ROOT}")
print(f"Database path: {DB}")
print(f"Input data folder: {INPUT_DIR}")
print(f"Reports folder: {OUTPUT_DIR}")


# --- 2. FUNCTION FOR DATA LOADING (EXTRACT & LOAD) ---
def load_csv_to_sqlite(db_path):
    """Reads CSV files from 'sample_input' folder and loads them into SQLite database."""
    conn = sqlite3.connect(db_path)
    
    try:
        orders = pd.read_csv(INPUT_DIR / "sample_orders.csv", parse_dates=['order_date'], low_memory=False)
        products = pd.read_csv(INPUT_DIR / "sample_products.csv", low_memory=False)
    except FileNotFoundError as e:
        print(f"ERROR: CSV file not found. Please check if 'sample_orders.csv' and 'sample_products.csv' exist in folder '{INPUT_DIR}'.")
        raise e

    # To be sure, let's print the column names from products CSV
    print("\nColumns in 'sample_products.csv':", products.columns.tolist())

    # Data cleaning and loading
    orders['customer_id'] = orders['customer_id'].fillna('guest')
    orders.to_sql('stg_orders', conn, if_exists='replace', index=False)
    products.to_sql('dim_products', conn, if_exists='replace', index=False)
    
    conn.commit()
    print("Data from CSV files has been successfully loaded into the database.")
    return conn

# --- 3. FUNCTION FOR DATA TRANSFORMATION (TRANSFORM) ---
def transform(conn):
    """Executes SQL transformations to normalize the data."""
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS orders;
    CREATE TABLE orders AS
    SELECT
      order_id,
      order_date,
      customer_id
    FROM stg_orders;
    
    DROP TABLE IF EXISTS order_items;
    CREATE TABLE order_items AS
    SELECT
      order_id,
      product_id,
      quantity,
      unit_price,
      quantity * unit_price AS line_total
    FROM stg_orders;
    """)
    conn.commit()
    print("Data transformations have been applied.")

# --- 4. FUNCTION FOR CREATING REPORTS (REPORTS) ---
def reports(conn):
    """Generates reports and saves them as CSV files in the 'outputs' folder."""
    # Monthly revenue report
    df_month = pd.read_sql_query("""
    SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.line_total) as revenue, COUNT(DISTINCT o.order_id) as orders
    FROM orders o
    JOIN order_items oi USING(order_id)
    GROUP BY month
    ORDER BY month;
    """, conn)
    # Save to the correct OUTPUT_DIR folder
    df_month.to_csv(OUTPUT_DIR / "monthly_revenue.csv", index=False)
    
    # Top products report
    # NOTE: Replace 'p.name' with the correct column name from your products CSV
    df_top = pd.read_sql_query("""
    SELECT
      p.product_name AS product_name,
      SUM(oi.line_total) as revenue,
      SUM(oi.quantity) as qty_sold
    FROM order_items oi
    LEFT JOIN dim_products p ON p.product_id = oi.product_id
    GROUP BY 1
    ORDER BY revenue DESC;
    """, conn)
    # Save to the correct OUTPUT_DIR folder
    df_top.to_csv(OUTPUT_DIR / "top_products.csv", index=False)
    
    print(f"Reports have been generated and saved to '{OUTPUT_DIR}'.")

# --- 5. MAIN SCRIPT EXECUTION ---
if __name__ == "__main__":
    # Correct way to delete file, compatible with older Python versions
    try:
        DB.unlink()
        print(f"\nOld database deleted: {DB}")
    except FileNotFoundError:
        pass  # File doesn't exist, do nothing

    # Execute the entire process
    connection = None
    try:
        connection = load_csv_to_sqlite(DB)
        transform(connection)
        reports(connection)
        print("\n✅ Process completed successfully!")
    except Exception as e:
        print(f"\n❌ An error occurred during execution: {e}")
    finally:
        if connection:
            connection.close()

