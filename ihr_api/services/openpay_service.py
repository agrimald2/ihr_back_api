import os
import openpay
from ihr_api import models

openpay.verify_ssl_certs = False
openpay.production = False
openpay.country = 'pe'


def generate_token(data, billing_account: models.BillingAccount) -> str:
    openpay.merchant_id = os.environ.get(str(billing_account.key_1))
    openpay.api_key = os.environ.get(str(billing_account.key_2))

    try:
        card = data.get('number', None)
        month_year = data.get('month_year', None)
        month, year = month_year.split('/')
        ccv = data.get('cvc', None)
        print(card, month, year, ccv)
        token = openpay.Token.create(
            card_number=card,
            holder_name="Juan Perez Nuñez",
            expiration_year=year,
            expiration_month=month,
            cvv2=ccv
        )

        return token.id
    except openpay.error.CardError as e:
        return "-"


def create_payment(source_id: str, sale: models.Sale, payment_link: models.PaymentLink, billing_account: models.BillingAccount) -> bool:
    openpay.merchant_id = os.environ.get(str(billing_account.key_1))
    openpay.api_key = os.environ.get(str(billing_account.key_2))

    amount = sale.payment.amount if sale else payment_link.amount
    reference = sale.reference if sale else payment_link.reference

    try:
        charge = openpay.Charge.create_as_merchant(
            method="card",
            amount=amount,
            currency='PEN',
            description="Testing card charges from python",
            order_id=reference,
            device_session_id="kjsadkjnnkjfvknjdfkjnvdkjnfvkj",
            source_id=source_id,
            customer={
                "name": "Heber",
                "last_name": "Robles",
                "email": "xxxxx@example.com",
                "phone_number": "4429938834",
                "address": {
                    "city": "Queretaro",
                    "state": "Queretaro",
                    "line1": "Calle de las penas no 10",
                    "postal_code": "15036",
                    "line2": "col. san pablo",
                    "line3": "entre la calle de la alegria y la calle del llanto",
                    "country_code": "PE"
                }
            }
        )
    except openpay.error.CardError as e:
        print(e)
        return False

    return charge.status == 'completed'
