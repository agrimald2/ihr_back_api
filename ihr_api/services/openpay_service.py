import os
import openpay
from ihr_api import models

openpay.api_key = os.environ.get('OPENPAY_SECRET_KEY')
openpay.verify_ssl_certs = False
openpay.merchant_id = os.environ.get('OPENPAY_MERCHANT_ID')
openpay.production = False
openpay.country = 'pe'


def generate_token(data) -> str:
    try:
        card = data.get('card', None)
        month_year = data.get('month_year', None)
        month, year = month_year.split('/')
        ccv = data.get('ccv', None)
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


def create_payment(source_id: str, sale: models.Sale) -> bool:
    try:
        charge = openpay.Charge.create_as_merchant(
            method="card",
            amount=sale.sub_total,
            currency='PEN',
            description="Testing card charges from python",
            order_id=sale.reference,
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
