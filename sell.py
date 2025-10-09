from royalty.trigger import trigger_royalty

def execute_sell(trade):
    # Core sell logic
    sell_value = trade.asset_price * trade.quantity
    trigger_royalty(trade.id, trade.asset, sell_value)
    # Proceed with sell execution
    trade.status = "sold"
    trade.timestamp = get_current_time()
    return trade

