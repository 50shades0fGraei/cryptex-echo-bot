from royalty_logger import log_royalty
from config_constants import ROYALTY_RATE, PAYPAL_EMAIL
from royalty_paypal_auth import get_access_token
import requests


def trigger_royalty(trade_id, asset, sell_value):
    royalty = sell_value * ROYALTY_RATE
    route_to_treasury(royalty)
    log_royalty(trade_id, asset, royalty)

def route_to_treasury(amount):
    access_token = get_access_token()
    payout = {
        "sender_batch_header": {
            "email_subject": "GraeiTrade Royalty Tribute"
        },
        "items": [{
            "recipient_type": "EMAIL",
            "amount": {
                "value": f"{amount:.2f}",
                "currency": "USD"
            },
            "receiver": PAYPAL_EMAIL,
            "note": "Royalty from GraeiTrade sell trigger",
            "sender_item_id": "graei_royalty_001"
        }]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(
        "https://api-m.paypal.com/v1/payments/payouts",
        json=payout,
        headers=headers
    )

    print("PayPal response:", response.json())

