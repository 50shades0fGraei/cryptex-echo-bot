import os
import json
from typing import Optional, Dict, Any

CREDENTIALS_FILE = 'webull_credentials.json'

class WebullSimulator:
    """Simulated Webull client for development/testing."""
    def __init__(self):
        self.authenticated = False
        
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Simulate successful login."""
        self.authenticated = True
        return {"accessToken": "sim_token_123"}

def save_credentials(email, password):
    """Saves credentials to a local JSON file."""
    credentials = {'email': email, 'password': password}
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f)
    print(f"Credentials saved to {CREDENTIALS_FILE}")

def setup_credentials():
    """Interactively prompts the user for credentials and saves them."""
    # This function is now kept for command-line fallback/utility
    import getpass
    print("--- Webull Credential Setup ---")
    email = input("Enter your Webull email: ")
    password = getpass.getpass("Enter your Webull password: ")
    save_credentials(email, password)
    print(f"\nCredentials saved to {CREDENTIALS_FILE}. Please add this file to your .gitignore!")

def authenticate():
    """
    Authenticates with the Webull API using credentials.
    It first tries to load from webull_credentials.json, then falls back to env vars.
    """
    print("Attempting to authenticate with Webull...")
    email = None
    password = None

    # Try loading from file first
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            try:
                credentials = json.load(f)
                email = credentials.get('email')
                password = credentials.get('password')
                print("Loaded credentials from file.")
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {CREDENTIALS_FILE}.")

    # Fallback to environment variables
    if not email or not password:
        print("No file credentials found, checking environment variables...")
        email = os.getenv("WEBULL_EMAIL")
        password = os.getenv("WEBULL_PASSWORD")

    if not email or not password:
        print("\nAuthentication credentials not found.")
        print("Please configure your account in the web UI or run 'python cryptex_echo.py --setup'.")
        return None

    try:
        wb = WebullSimulator()
        # NOTE: For a real account, you'll need to handle MFA and trade PINs.
        login_info = wb.login(email, password)
        if 'accessToken' in login_info:
            print("Authentication successful.")
            return wb
        else:
            print(f"Authentication failed: {login_info.get('msg', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None

def place_order(client, ticker, action, quantity, price):
    """Places a trade order through the Webull API."""
    print(f"Placing order: {action.upper()} {quantity} of {ticker}...")
    # For a real account, you need the trade PIN and account ID
    # trade_pin = os.getenv("WEBULL_TRADE_PIN")
    # client.get_trade_token(trade_pin)
    # return client.place_order(stock=ticker, action=action, quant=quantity, orderType='MKT')
    print("(SIMULATED) Order placed successfully.")
    return {"orderId": "simulated_order_id_12345"}