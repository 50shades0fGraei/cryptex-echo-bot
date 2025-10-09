import random

# Initial Setup
initial_investment = 500
days_in_quarter = 90
daily_fluctuation_in_passer1 = 0.005
daily_fluctuation_in_passer2 = -0.005
daily_fluctuation_runner = 0.10
profit_boost = 0.05

starting_capital = {
    "runner": 200,
    "in_passer1": 150,
    "in_passer2": 150
}

initial_prices = {
    "in_passer1": 1000,
    "in_passer2": 30000,
    "runner": 2000
}

capital = starting_capital.copy()
current_prices = initial_prices.copy()
monthly_pool = 0
month_profits = [0]
month = 1

# Currency Class
class Currency:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.positions = []

    def buy(self, price, units, capital):
        cost = price * units
        if capital >= cost:
            self.positions.append((price, units))
            return cost
        return 0

    def sell(self, price, units_to_sell):
        if not self.positions:
            return 0
        proceeds = 0
        sold_units = 0
        new_positions = []
        for buy_price, units in self.positions:
            if sold_units < units_to_sell:
                sell_units = min(units, units_to_sell - sold_units)
                sold_units += sell_units
                proceeds += sell_units * price
                remaining_units = units - sell_units
                if remaining_units > 0:
                    new_positions.append((buy_price, remaining_units))
            else:
                new_positions.append((buy_price, units))
        self.positions = new_positions
        return proceeds

currencies = {name: Currency(name, price) for name, price in initial_prices.items()}

# Trading Logic
def trade_overlap_zones():
    global capital, monthly_pool
    runner_price = current_prices["runner"]
    in_passer1_price = current_prices["in_passer1"]
    in_passer2_price = current_prices["in_passer2"]

    # Buy Runner near In-Passer 1
    if abs(runner_price - in_passer1_price) / in_passer1_price <= 0.10 and runner_price < in_passer1_price:
        units_to_buy = capital["runner"] / runner_price
        cost = currencies["runner"].buy(runner_price, units_to_buy, capital["runner"])
        capital["runner"] -= cost

    # Sell Runner near In-Passer 2
    if abs(runner_price - in_passer2_price) / in_passer2_price <= 0.10 and runner_price >= in_passer2_price * 0.5:
        total_units = sum(units for _, units in currencies["runner"].positions)
        if total_units > 0:
            units_to_sell = min(1, total_units)
            proceeds = currencies["runner"].sell(runner_price, units_to_sell)
            capital["runner"] += proceeds
            profit = proceeds - (runner_price * units_to_sell * 0.9)
            if profit > 0:
                pool_amount = profit * 0.5
                reinvest_amount = profit * 0.5
                capital["runner"] += reinvest_amount
                monthly_pool += pool_amount

# Main Loop
for day in range(days_in_quarter):
    # Update Prices
    current_prices["in_passer1"] *= (1 + daily_fluctuation_in_passer1)
    current_prices["in_passer2"] *= (1 + daily_fluctuation_in_passer2)
    direction = random.choice([-1, 1])
    current_prices["runner"] *= (1 + daily_fluctuation_runner * direction)
    current_prices["runner"] = max(1000, min(15000, current_prices["runner"]))

    # Trade 3 times per day
    for _ in range(3):
        trade_overlap_zones()

    # Monthly Adjustments
    if day % 30 == 0:
        for passer in ["in_passer1", "in_passer2"]:
            if capital[passer] > 0 and random.random() > 0.5:
                units_to_buy = capital[passer] / current_prices[passer]
                cost = currencies[passer].buy(current_prices[passer], units_to_buy, capital[passer])
                capital[passer] -= cost

    # Profit Boost
    for curr_name in ["runner", "in_passer1", "in_passer2"]:
        initial = starting_capital[curr_name]
        profit = capital[curr_name] - initial
        if profit > 0:
            capital[curr_name] *= (1 + profit_boost)

    # Monthly Boost
    if day % 30 == 0 and day > 0:
        monthly_boost = sum(month_profits[-1] * 0.5 for _ in range(3) if month_profits)
        for curr_name in starting_capital:
            capital[curr_name] += monthly_boost * (starting_capital[curr_name] / initial_investment)
        month += 1

    # Track Monthly Profits
    if day % 30 == 29:
        month_profit = sum(capital[curr] - starting_capital[curr] for curr in starting_capital)
        month_profits.append(month_profit)

# Final Results
total = sum(capital.values()) + monthly_pool
quarterly_roi = (total / initial_investment - 1) * 100

print(f"Capital Breakdown: {capital}")
print(f"Monthly Pool: ${monthly_pool:.2f}")
print(f"Total: ${total:.2f}")
print(f"Quarterly ROI: {quarterly_roi:.2f}%")
