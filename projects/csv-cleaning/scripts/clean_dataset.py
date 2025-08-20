# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 20:41:05 2025

@author: DanielKolchakov
"""

import pandas as pd
import numpy as np

df = pd.read_csv('input_sample.csv')

#2. SECOND - Defining the cleaning function
def clean_dataset(df):
    """
    Function for complete dataset cleaning
    """
    df_clean = df.copy()
    
    # 1. Cleaning text fields
    text_columns = ['customer_name', 'product']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip()
            df_clean[col] = df_clean[col].replace('', np.nan)
    
    # 2. Cleaning special missing values
    df_clean = df_clean.replace('\\N', np.nan)
    
    # 3. Convert data types
    if 'order_date' in df_clean.columns:
        df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], errors='coerce')
    
    if 'price' in df_clean.columns:
        df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    
    # 4. Dealing with missing values
    if 'customer_name' in df_clean.columns:
        df_clean['customer_name'].fillna('Unknown Customer', inplace=True)
    
    if 'order_date' in df_clean.columns:
        if df_clean['order_date'].notna().any():
            fill_date = df_clean['order_date'].mode()[0]
            df_clean['order_date'].fillna(fill_date, inplace=True)
    
    # 5. Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # 6. Reset index
    df_clean = df_clean.reset_index(drop=True)
    
    return df_clean

# 3. THIRD - Applying the cleaning
df_final = clean_dataset(df)

print("\nFinal cleaned dataset:")
print(df_final)
print(f"\nData information:")
print(df_final.info())    

if __name__ == "__main__":
    df_final.to_csv('../cleaned_orders.csv', index=False)
    print("Данните са запазени в cleaned_orders.csv")