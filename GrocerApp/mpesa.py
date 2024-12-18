import requests
from django.conf import settings

def initiate_mpesa_payment(phone_number, amount):
    # URL and headers for Mpesa API
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {settings.MPESA_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    # Payload for the Mpesa API request
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": settings.MPESA_PASSWORD,
        "Timestamp": settings.MPESA_TIMESTAMP,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "Grocery",
        "TransactionDesc": "Grocery Payment",
    }

    # Send the request to Mpesa API
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def lipa_na_mpesa_online(phone_number, amount):
    # Your implementation for lipa_na_mpesa_online
    pass
