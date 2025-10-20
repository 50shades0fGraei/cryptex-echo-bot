import datetime
import json
import os
from typing import List, Dict, Any

LOG_PATH = "royalty/logs/royalty_log.jsonl"  # Use .jsonl for JSON Lines format

def log_royalty(trade_id, asset, amount):
    """Appends a new royalty record to the log file in a safe, atomic manner."""

    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        "trade_id": trade_id,
        "asset": asset,
        "royalty": round(amount, 2),
        "timestamp": timestamp
    }

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    # Append a single line of JSON. This is an atomic operation on most OS.
    with open(LOG_PATH, "a") as file:
        file.write(json.dumps(log_entry) + "\n")

def read_log() -> List[Dict[str, Any]]:
    """Reads all royalty records from the log file, skipping any corrupted lines."""
    try:
        with open(LOG_PATH, "r") as f:
            entries = []
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    # Skip corrupted or empty lines
                    continue
            return entries
    except FileNotFoundError:
        return []
