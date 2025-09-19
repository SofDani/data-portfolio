# 1. Импортиране на необходимите библиотеки
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt


    # 2. Loading and preparing historical data
data = pd.read_csv('BANK URALSIB Stock Price History.csv', parse_dates=['Date'], dayfirst=True, index_col='Date')


    # Make sure that the 'Price' column is numeric. If there are non-numeric values, they will become NaN.
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')

    # Remove rows with missing values ​​in 'Price'.
    data.dropna(subset=['Price'], inplace=True)

    # Sort the data by date in ascending order (from oldest to newest).
    data.sort_index(inplace=True)

    # Checking if DataFrame is not empty after loading and cleaning.
    if data.empty:
         raise ValueError("DataFrame е празен след зареждане и почистване. Проверете CSV файла.")
    print(f"Данните са заредени успешно. Брой наблюдения: {data.shape}")
    #print("Първи 5 реда:\n", data.head())
    #print("Последни 5 реда:\n", data.tail())


# --- Изчислителна секция ---

# 3. Calculating CAGR (Compound Annual Growth Rate) -> mu (Expected Return)
# The period in days between the first and last date in the data.
# I use .iloc for positional access to avoid index problems
start_price = data['Price'].iloc[0]
end_price = data['Price'].iloc[-1]
start_date = data.index[0]
end_date = data.index[-1]
days = (end_date - start_date).days

# Validity period check
if days <= 0 or start_price <= 0:
    print("Предупреждение: Невалиден период или начална цена за изчисляване на CAGR. Задаваме mu = 0.")
    cagr = 0.0
else:
    # The CAGR formula converted to an annual rate
    cagr = ((end_price / start_price) ** (365.0 / days)) - 1

mu = cagr # The average expected annual return.
print(f'Изчислен CAGR (mu): {mu:.4f} ({mu*100:.2f}%)')

# 4. Calculating annual volatility -> vol
# calculating the daily percentage changes in price.
returns = data['Price'].pct_change()
# Remove the first value (NaN) that is obtained with pct_change().
returns = returns.dropna()

# Checking if there are calculated returns
if returns.empty:
     print("Предупреждение: Не могат да се изчислят дневни възвръщаемости. Задаваме vol = 0.")
     vol = 0.0
else:
     # The standard deviation of daily returns, annualized by multiplying by sqrt(252).
# 252 is the approximate number of trading days in a year.
     vol = returns.std() * sqrt(252)

print(f"Изчислена годишна волатилност (vol): {vol:.4f} ({vol*100:.2f}%)")

# --- Секция за симулация на Монте Карло ---

# 5. Дефиниране на параметрите на симулацията
S = data['Price'].iloc[-1] # Starting price (last available real price).
T = 252                  # Number of trading days for simulation (1 year).
num_simulations = 1000   # Number of simulations (paths) to generate.

print(f'\n--- Параметри на симулацията ---')
print(f'Начална цена (S): {S:.4f}')
print(f'Период на симулация (T): {T} дни')
print(f'Брой симулации: {num_simulations}')

# 6. Изпълнение на симулациите
result = [] # List for storing the final prices from each simulation.

plt.figure(figsize=(12, 7)) # Създаване на фигура за графиката с пътеките(path).

for i in range(num_simulations):
    # Generate random daily returns.
    # We use a normal distribution with mean (mu/T) and standard deviation (vol/sqrt(T)).
    # We add 1 to get multiplicative factors (1 + daily return).
    daily_returns_sim = np.random.normal(mu / T, vol / sqrt(T), T) + 1

    # Generating the price series (path).
    price_list = [S] # Започваме със стартовата цена.
    # For each daily return generated, we calculate the next price.
    for x in daily_returns_sim:
        price_list.append(price_list[-1] * x)

    # Add the final price from this simulation to the results list.
    result.append(price_list[-1])

    # Plotting the graph of the current price path.
# alpha=0.1 makes the lines semi-transparent to show their density.
    plt.plot(price_list, alpha=0.1, color='blue')

# --- Визуализация и Анализ ---

# 7. Show chart with all simulated price paths
plt.title(f'Монте Карло Симулация: {num_simulations} Ценови Пътеки за Bank Uralsib (USBN) за {T} дни')
plt.xlabel('Търговски Дни')
plt.ylabel('Симулирана Цена (RUB)')
plt.grid(True, alpha=0.3) # Adding a grid for better readability.
plt.show() # Rendering the graph.

# 8. Constructing a histogram of final prices
plt.figure(figsize=(10, 6)) # New shape for the histogram.
# bins=50 divides the data into 50 intervals (columns).
plt.hist(result, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Разпределение на Крайните Цени след Симулацията')
plt.xlabel('Крайна Цена (RUB)')
plt.ylabel('Честота')

# 9. Calculation and display of statistical indicators
mean_price = np.mean(result)      # Average final price from all simulations.
quantile_5 = np.percentile(result, 5)   # 5th percentile (price below which 5% of results fall).
quantile_95 = np.percentile(result, 95) # 95th percentile (price below which 95% of the results fall).

print(f'\n--- Анализ на резултатите ({num_simulations} симулации) ---')
print(f'Средна крайна цена: {mean_price:.4f} RUB')
print(f'5% квантил (песимистичен): {quantile_5:.4f} RUB')
print(f'95% квантил (оптимистичен): {quantile_95:.4f} RUB')

# Add mean and quantile lines to the histogram
plt.axvline(mean_price, color='black', linestyle='solid', linewidth=2, label=f'Средна: {mean_price:.2f}')
plt.axvline(quantile_5, color='red', linestyle='dashed', linewidth=2, label=f'5% квантил: {quantile_5:.2f}')
plt.axvline(quantile_95, color='green', linestyle='dashed', linewidth=2, label=f'95% квантил: {quantile_95:.2f}')
plt.legend() # Show legend with line explanations.
plt.grid(True, alpha=0.3)
plt.show() # Show histogram.