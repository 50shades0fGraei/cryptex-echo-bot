from flask import Flask, render_template_string
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <h1>🧿 Cryptex Echo Dashboard</h1>
    <ul>
        <li><a href="/pearls">View Pearl Log</a></li>
        <li><a href="/royalties">View Royalty Log</a></li>
    </ul>
    """)

@app.route('/pearls')
def pearls():
    try:
        with open("PEARL_LOG.md") as f:
            entries = f.readlines()
    except:
        entries = ["No pearls yet."]
    return render_template_string("""
    <h2>📜 Pearl Log</h2>
    <pre>{{ pearls }}</pre>
    <a href="/">Back</a>
    """, pearls="".join(entries))

@app.route('/royalties')
def royalties():
    log_file_path = "royalty/logs/royalty_log.jsonl"
    data = []
    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        data.append(entry)
                    except json.JSONDecodeError:
                        # Skip corrupted or empty lines
                        continue
        if not data: # If file exists but is empty or only has corrupted lines
            data = [{"timestamp": str(datetime.now()), "trade_id": "N/A", "asset": "No royalties yet.", "royalty": 0.0}]
    except FileNotFoundError:
        data = [{"timestamp": str(datetime.now()), "trade_id": "N/A", "asset": "No royalties yet.", "royalty": 0.0}]
    except Exception as e: # Catch broader exceptions
        print(f"Error reading royalty log: {e}")
        data = [{"timestamp": str(datetime.now()), "trade_id": "N/A", "asset": f"Error: {e}", "royalty": 0.0}]
    return render_template_string("""
    <h2>💰 Royalty Log</h2>
    {% for entry in data %}
        <p>{{ entry.timestamp }} :: Trade ID: {{ entry.trade_id }}, Asset: {{ entry.asset }}, Royalty: ${{ entry.royalty | round(2) }}</p>
    {% endfor %}
    <a href="/">Back</a>
    """, data=data)

if __name__ == '__main__':
    app.run(debug=True)
