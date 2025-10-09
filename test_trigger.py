from trade_sell import execute_sell

class Trade:
    def __init__(self, id, asset, asset_price, quantity):
        self.id = id
        self.asset = asset
        self.asset_price = asset_price
        self.quantity = quantity
        self.status = None
        self.timestamp = None

def get_current_time():
    from datetime import datetime
    return datetime.now().isoformat()

# Inject get_current_time into global scope if needed
globals()["get_current_time"] = get_current_time

# Create a test trade
test_trade = Trade(
    id="graei-test-001",
    asset="MythicPearl",
    asset_price=100.00,
    quantity=1
)

# Execute the sell
result = execute_sell(test_trade)
print("Sell Result:", vars(result))
