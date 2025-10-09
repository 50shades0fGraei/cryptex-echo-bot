from fetch_prices import get_price

def echo_trade(runner, low_pass, high_pass):
    r_price = get_price(runner)
    l_price = get_price(low_pass)
    h_price = get_price(high_pass)

    if abs(r_price - l_price) < 5:
        return f"🔁 Buy {runner} near Low-Passer ({low_pass})"
    elif abs(r_price - h_price) < 5:
        return f"💰 Sell {runner} near High-Passer ({high_pass})"
    else:
        return "🌌 No trade — Echo not aligned"

