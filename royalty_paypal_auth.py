import requests
from config_constants import PAYPAL_CLIENT_ID, PAYPAL_SECRET

def get_access_token():
    response = requests.post(
        "https://api-m.paypal.com/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US"
        },
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"}
    )
    return response.json()["access_token"]

