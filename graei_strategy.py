def trade_overlap_zones(current_prices, capital, currencies, monthly_pool):
    runner_price = current_prices["runner"]
    in_passer1_price = current_prices["in_passer1"]
    in_passer2_price = current_prices["in_passer2"]

    # Buy Runner near In-Passer 1
    if abs(runner_price - in_passer1_price) / in_passer1_price <= 0.05 and runner_price < in_passer1_price:
        units_to_buy = capital["runner"] / runner_price
        cost = currencies["runner"].buy(runner_price, units_to_buy, capital["runner"])
        capital["runner"] -= cost

    # Sell Runner near In-Passer 2
    if abs(runner_price - in_passer2_price) / in_passer2_price <= 0.05 and runner_price >= in_passer2_price * 0.5:
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

    return monthly_pool
