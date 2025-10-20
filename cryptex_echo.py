f"""
Cryptex Echo Bot — Sovereign Artifact  
Licensed under Cryptex Echo Sovereign License v1.0  
© 2025 Randall Lujan. All rights reserved.
"""

from trade_logic import echo_trade
from pearl_log import pearlize
from webull_adapter import authenticate, place_order
import json

def run_echo():
    # Load configuration from file
    # Authenticate with the trading platform
    print("Initializing Cryptex Echo Bot...")
    client = authenticate()

    # Load trading strategy configuration from file
    with open('config.json', 'r') as f:
        config = json.load(f)

    runner = config.get("runner", "TSLA") # Default to TSLA if not found
    low_pass = config.get("low_pass", "F")
    high_pass = config.get("high_pass", "RIVN")

    # Run echo trade logic
    event = echo_trade(runner, low_pass, high_pass)
    print(event)

    # If a trade is suggested, execute it
    if "Buy" in event:
        # In a real scenario, you'd determine quantity and price differently
        place_order(client, ticker=runner, action="buy", quantity=1, price=0) # price=0 for market order
        event += " - Order Placed!"
    elif "Sell" in event:
        place_order(client, ticker=runner, action="sell", quantity=1, price=0) # price=0 for market order
        event += " - Order Placed!"

    # Log the event as a pearl
    pearlize(event)

if __name__ == "__main__":
    run_echo()
