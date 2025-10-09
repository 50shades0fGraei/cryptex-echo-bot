portfolio = {"TSLA": 0, "cash": 10000}

def simulate_trade(action, ticker, price):
    qty = 0
    if action == "buy":
        qty = int(portfolio["cash"] // price)
        portfolio[ticker] += qty
        portfolio["cash"] -= qty * price
    elif action == "sell":
        qty = portfolio.get(ticker, 0)
        portfolio["cash"] += qty * price
        portfolio[ticker] = 0

    return f"{action.upper()} {qty} shares of {ticker} at ${price:.2f}"

