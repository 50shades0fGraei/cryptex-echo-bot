import datetime
import json
import os

LOG_PATH = "royalty/logs/royalty_log.json"

def log_royalty(trade_id, asset, amount):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        "trade_id": trade_id,
        "asset": asset,
        "royalty": round(amount, 2),
        "timestamp": timestamp
    }

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r+") as file:
            data = json.load(file)
            data.append(log_entry)
            file.seek(0)
            json.dump(data, file, indent=2)
    else:
        with open(LOG_PATH, "w") as file:
            json.dump([log_entry], file, indent=2)

def read_log():
    try:
        with open("royalty_log.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
