from royalty_trigger import trigger_royalty
from datetime import datetime

def get_current_time():
    return datetime.now().isoformat()

def execute_sell(trade):
    # Core sell logic
    sell_value = trade.asset_price * trade.quantity
    trigger_royalty(trade.id, trade.asset, sell_value)
    # Proceed with sell execution
    trade.status = "sold"
    trade.timestamp = get_current_time()
    return trade
