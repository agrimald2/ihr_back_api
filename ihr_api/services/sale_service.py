from ihr_api import models
from ihr_api.services import openpay_service
import string
import random
from rest_framework.request import Request


def process_request(request: Request):
    data = request.data.copy()
    cart = data.get('cart_info', None)
    cart_total = data.get('cart_total', None)
    source_id = data.get('token_id', None)
    payment_method = data.get('method', None)
    billing_info = data.get('billing_info', None)
    shipping_info = data.get('shipping_info', None)

    print(cart)
    print(source_id)
    print(payment_method)
    print(billing_info)
    print(shipping_info)
    return cart, cart_total, shipping_info, payment_method, billing_info, source_id


def make_sale(cart, cart_total, shipping_info, payment_method: int, billing_info, source_id, user: models.User) -> bool:
    payment_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    payment = models.Payment.objects.create(
        reference=payment_reference,
        amount=cart_total,
        payment_method=payment_method,
        status=models.Payment.STATUS_PENDING
    )

    address = f"{shipping_info['street']}, {shipping_info['city']}, {shipping_info['country']}, {shipping_info['zip_code']}"

    sale_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    sale = models.Sale.objects.create(
        reference=sale_reference,
        user=user,
        address=address,
        first_name=shipping_info['first_name'],
        last_name=shipping_info['last_name'],
        phone_number=shipping_info['phone'],
        sub_total=cart_total,
        payment=payment
    )

    for item in cart:
        models.SaleItem.objects.create(
            sale=sale,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price'],
            sub_total=item['sub_total']
        )

    payment_success = False

    if payment_method == models.Payment.METHOD_OPEN_PAY:
        payment_success = openpay_service.create_payment(cart_total, 'PEN', openpay_service.generate_token(), sale_reference)
    elif payment_method == models.Payment.METHOD_CRYPTO:
        payment_success = False

    if payment_success and sale.status == models.Sale.SALE_PENDING_PAYMENT and sale.payment.status == models.Payment.STATUS_PENDING:
        payment.status = models.Payment.STATUS_CONFIRMED
        payment.save()

        sale.status = models.Sale.SALE_CONFIRMED
        sale.save()
        return True
    return False
