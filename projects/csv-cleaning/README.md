# CSV Cleaning — Enhanced Demo Project

## 🎯 Цел на проекта
Този проект демонстрира **пълно почистване на CSV dataset** с помощта на Python (pandas & numpy).  
Скриптът автоматизира основните стъпки при обработка на сурови данни:  
- премахване на излишни интервали и празни стойности  
- замяна на специални null маркери (`\N`, `NA`, празни полета)  
- конвертиране на типове данни (дата, цена)  
- запълване на липсващи стойности с дефолти или най-често срещаните  
- премахване на дубликати и ресет на индекса  

## 🛠 Използвани технологии
- **Python 3**  
- **pandas** — манипулация на данни  
- **numpy** — работа с null стойности  

## 📂 Структура на проекта
csv-cleaning/
├─ input_sample.csv # примерни сурови данни
├─ cleaned_orders.csv # почистени данни (output)
├─ scripts/
│ └─ clean_dataset.py # основен Python скрипт за почистване
└─ README.md # документация (този файл)


## ▶️ Как да стартирате скрипта

**1. Клонирайте или свалете репозиторито**
```bash
git clone https://github.com/<SofDani>/data-portfolio.git
cd data-portfolio/projects/csv-cleaningcd data-portfolio/projects/csv-cleaning

2. Инсталирайте
pip install pandas numpy

3. Стартирайте скрипта
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


Автор: Даниел Василев Колчаков
📧 Email: danielkolchakov97@gmail.com
🔗 LinkedIn: daniel-kolchakov-799361182