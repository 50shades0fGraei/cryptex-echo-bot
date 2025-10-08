# Cryptex Echo Bot — Ritual Core
import yfinance as yf

# Assets
runner = yf.Ticker("TSLA")
low_pass = yf.Ticker("F")
high_pass = yf.Ticker("RIVN")

def get_price(ticker):
    return ticker.history(period="1d")["Close"].iloc[-1]

def echo_trade():
    r_price = get_price(runner)
    l_price = get_price(low_pass)
    h_price = get_price(high_pass)

    print(f"Runner: {r_price}, Low: {l_price}, High: {h_price}")

    if abs(r_price - l_price) < 5:
        print("🔁 Buy Runner near Low-Passer")
    elif abs(r_price - h_price) < 5:
        print("💰 Sell Runner near High-Passer")
    else:
        print("🌌 No trade — Echo not aligned")

echo_trade()
