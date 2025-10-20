from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from pydantic import BaseModel
import os

app = FastAPI()

# Allow CORS for your frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # The default Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

CONFIG_PATH = 'config.json'

@app.get("/")
def read_root():
    return {"message": "GraeiTrade backend is alive"}

@app.get("/pearls")
def get_pearls():
    try:
        with open("PEARL_LOG.md") as f:
            content = f.read()
    except FileNotFoundError:
        content = "No pearls yet."
    return {"content": content}

@app.get("/royalties")
def get_royalties():
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
    except Exception as e: # Catch broader exceptions for file operations
        print(f"Error reading royalty log: {e}")
        data = [{"timestamp": str(datetime.now()), "trade_id": "N/A", "asset": f"Error: {e}", "royalty": 0.0}]
    return data

@app.post("/chat")
async def handle_chat(chat_message: ChatMessage):
    user_message = chat_message.message.lower().strip()
    response_message = "I'm not sure how to handle that. Try asking me to 'change the runner to [TICKER]' or 'what is the current config?'."

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)

        if "change runner to" in user_message:
            new_runner = user_message.split("change runner to")[-1].strip().upper()
            if new_runner:
                config['runner'] = new_runner
                response_message = f"Configuration updated. Runner is now {new_runner}."
            else:
                response_message = "Please specify a ticker for the runner."
        elif "change low pass to" in user_message:
            new_low_pass = user_message.split("change low pass to")[-1].strip().upper()
            if new_low_pass:
                config['low_pass'] = new_low_pass
                response_message = f"Configuration updated. Low-Pass is now {new_low_pass}."
            else:
                response_message = "Please specify a ticker for the low-pass."
        elif "change high pass to" in user_message:
            new_high_pass = user_message.split("change high pass to")[-1].strip().upper()
            if new_high_pass:
                config['high_pass'] = new_high_pass
                response_message = f"Configuration updated. High-Pass is now {new_high_pass}."
            else:
                response_message = "Please specify a ticker for the high-pass."
        elif "what is the current config" in user_message or "show config" in user_message:
            response_message = f"Current config: Runner is {config.get('runner')}, Low-Pass is {config.get('low_pass')}, and High-Pass is {config.get('high_pass')}."
        elif "hello" in user_message or "hi" in user_message:
            response_message = "Hello! I am Graei, your trading bot assistant. How can I help you configure your strategy today?"

        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

    except Exception as e:
        response_message = f"Sorry, I encountered an error: {e}"

    return {"reply": response_message}
