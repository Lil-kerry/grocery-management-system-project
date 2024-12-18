from send_sms_email import send_sms

if __name__ == "__main__":
    phone_number = "0110866688"
    message = "Test SMS from GrocerEase"
    carrier = "safaricom"
    send_sms(phone_number, message, carrier)
