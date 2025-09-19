# CSV Cleaning — Enhanced Demo Project

## 🎯 Project goal
This project demonstrates complete cleaning of a CSV dataset using Python(pandas & numpy).
The script automates the main steps in raw data processing:
    - Removing extra spaces and empty values
    - Replacing evaluated null markers(\N, NA, empty fields)
    - Converting data types(data,price)
    - Filling missing values with defaults or the most common ones
    - Removing Post and resetting the index

##  Technologies used
- Python 3   
- pandas - data manipulation
- numpy -  working with null values

## Project structure
csv-cleaning/
- input_sample.csv # sample raw data
- cleaned_orders.csv # cleaned data (output)
- scripts/
     clean_dataset.py # basic Python script
         README.md # documentation


## How to start the script

1. Clone or download the repository
```bash
git clone https://github.com/<SofDani>/data-portfolio.git
cd data-portfolio/projects/csv-cleaning

2. Install
pip install pandas numpy

3. Run the script
python scripts/clean_pandas.py

Input:
order_id,customer_name,product,price,order_date
1, John Doe ,Dog Toy,12.5,2024-11-01
2,Jane Smith,Cat Toy,9.99,2024-11-02
3,John Doe,Dog Toy,12.5,2024-11-01
4, ,Baby Blanket,25.00,\N
5,Maria Ivanova,Pacifier,5.5,2024-10-30

Output:
order_id     customer_name          product  price order_date
0         1          John Doe       Dog Toy  12.50 2024-11-01
1         2        Jane Smith       Cat Toy   9.99 2024-11-02
2         3          John Doe       Dog Toy  12.50 2024-11-01
3         4  Unknown Customer  Baby Blanket  25.00 2024-11-01
4         5     Maria Ivanova      Pacifier   5.50 2024-10-30


Author: Daniel Kolchakov
 Email: danielkolchakov97@gmail.com
 LinkedIn: daniel-kolchakov-799361182