import os

import openpay

openpay.api_key = os.environ.get('OPENPAY_SECRET_KEY')
openpay.verify_ssl_certs = False
openpay.merchant_id = os.environ.get('OPENPAY_MERCHANT_ID')
openpay.production = False
openpay.country = 'pe'


def generate_token() -> str:
    token = openpay.Token.create(
        card_number="4111111111111111",
        holder_name="Juan Perez Nuñez",
        expiration_year="24",
        expiration_month="12",
        cvv2="110"
    )

    return token.id


def create_payment(amount: float, currency: str, source_id: str, sale_reference: str) -> bool:
    try:
        charge = openpay.Charge.create_as_merchant(
            method="card",
            amount=amount,
            currency=currency,
            description="Testing card charges from python",
            order_id=sale_reference,
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
