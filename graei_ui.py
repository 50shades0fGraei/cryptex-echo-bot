from flask import Flask, render_template_string
import json
from datetime import datetime

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
    try:
        with open("royalty/logs/royalty_log.json") as f:
            data = json.load(f)
    except:
        data = [{"timestamp": str(datetime.now()), "event": "No royalties yet."}]
    return render_template_string("""
    <h2>💰 Royalty Log</h2>
    {% for entry in data %}
        <p>{{ entry.timestamp }} :: {{ entry.event }}</p>
    {% endfor %}
    <a href="/">Back</a>
    """, data=data)

if __name__ == '__main__':
    app.run(debug=True)
