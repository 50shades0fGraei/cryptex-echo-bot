import random
from graei_strategy import trade_overlap_zones
from currency import Currency
from graei_constants import *

# Initialize
capital = starting_capital.copy()
positions = {key: [] for key in starting_capital}
current_prices = initial_prices.copy()
monthly_pool = 0
month_profits = [0]
day = 0
month = 1

currencies = {name: Currency(name, price) for name, price in initial_prices.items()}

# Main Loop
for day in range(days_in_quarter):
    # Update Prices
    current_prices["in_passer1"] *= (1 + daily_fluctuation_in_passer1)
    current_prices["in_passer2"] *= (1 + daily_fluctuation_in_passer2)
    direction = random.choice([-1, 1])
    current_prices["runner"] *= (1 + daily_fluctuation_runner * direction)
    current_prices["runner"] = max(1000, min(15000, current_prices["runner"]))

    # Trade
    for _ in range(3):  # 3 trades per day
        monthly_pool = trade_overlap_zones(current_prices, capital, currencies, monthly_pool)

    # Profit Boost
    for curr_name in ["runner", "in_passer1", "in_passer2"]:
        daily_profit = capital[curr_name] - (initial_investment * starting_capital[curr_name] / initial_investment)
        if daily_profit > 0:
            capital[curr_name] *= (1 + profit_boost)

    # Monthly Boost
    if day % 30 == 0 and day > 0:
        monthly_boost = sum(month_profits[-1] * 0.5 for _ in range(3) if month_profits)
        for curr_name in starting_capital:
            capital[curr_name] += monthly_boost * (starting_capital[curr_name] / initial_investment)
        month += 1

    # Track Monthly Profits
    if day % 30 == 29:
        month_profit = sum(capital[curr] - (initial_investment * starting_capital[curr] / initial_investment) for curr in starting_capital)
        month_profits.append(month_profit)

# Final Results
total = sum(capital.values()) + monthly_pool
quarterly_roi = (total / initial_investment - 1) * 100

print(f"Capital Breakdown: {capital}")
print(f"Monthly Pool: ${monthly_pool:.2f}")
print(f"Total: ${total:.2f}")
print(f"Quarterly ROI: {quarterly_roi:.2f}%")
