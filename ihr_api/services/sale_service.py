from ihr_api import models
from ihr_api.services import openpay_service
import string
import random


def make_sale(cart, address, payment_method: int, indications, user: models.User) -> bool:
    payment_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    payment = models.Payment.objects.create(
        reference=payment_reference,
        amount=cart.total,
        payment_method=payment_method,
        status=models.Payment.STATUS_PENDING
    )

    sale_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    sale = models.Sale.objects.create(
        reference=sale_reference,
        user=user,
        address=address,
        indications=indications,
        payment=payment
    )

    payment_success = False

    if payment_method == models.Payment.PAYMENT_METHODS.METHOD_CARD:
        payment_success = openpay_service.create_payment(cart.total, 'PEN', openpay_service.generate_token(), sale_reference)
    elif payment_method == models.Payment.PAYMENT_METHODS.METHOD_CRYPTO:
        payment_success = False

    if payment_success and sale.status == models.Sale.SALE_PENDING_PAYMENT and sale.payment.status == models.Payment.STATUS_PENDING:
        payment.status = models.Payment.STATUS_CONFIRMED
        payment.save()

        sale.status = models.Sale.SALE_CONFIRMED
        sale.save()
        return True
    return False
