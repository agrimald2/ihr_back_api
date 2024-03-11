import os
import mercadopago
from ihr_api import models


def generate_token(data, billing_account: models.BillingAccount) -> str:
    sdk = mercadopago.SDK(str(os.environ.get(str(billing_account.key_1))))

    card = data.get('number', None)
    month_year = data.get('month_year', None)
    month, year = month_year.split('/')
    ccv = data.get('cvc', None)
    print(card, month, year, ccv)
    token = sdk.card_token().create({
        "card_number": card,
        "security_code": ccv,
        "expiration_month": month,
        "expiration_year": 2000 + int(year),
        "cardholder": {
            "name": "APRO",
            "identification": {
                "dni": "123456789"
            }
        }
    })
    print(token)
    return token["response"]["id"]


def create_payment(source_id: str, sale: models.Sale, billing_account: models.BillingAccount) -> bool:
    sdk = mercadopago.SDK(str(os.environ.get(str(billing_account.key_1))))

    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': sale.payment.reference
    }

    payment_data = {
        "transaction_amount": sale.payment.amount,
        "token": source_id,
        "description": "ecommerce sale",
        "payment_method_id": 'visa',
        "installments": 1,
        "payer": {
            "email": 'mcoloniab18@gmail.com'
        }
    }
    result = sdk.payment().create(payment_data)
    print(result)
    return result["status"] == 201
