"""
Cryptex Echo Bot — Sovereign Artifact  
Licensed under Cryptex Echo Sovereign License v1.0  
© 2025 Randall Lujan. All rights reserved.
"""

from trade_logic import echo_trade
from pearl_log import pearlize
from royalty_trigger import royalty_trigger
from webull_adapter import authenticate, simulate_trade

def run_echo():
    # Authenticate with Webull
    authenticate()

    # Simulate a trade for AAPL
    simulate_trade('AAPL', 180.00)

    # Define asset trio for echo logic
    runner = "TSLA"
    low_pass = "F"
    high_pass = "RIVN"

    # Run echo trade logic
    event = echo_trade(runner, low_pass, high_pass)
    print(event)

    # Log pearl and trigger royalty
    pearlize(event)
    royalty_trigger("Echo Invocation")

if __name__ == "__main__":
    run_echo()
