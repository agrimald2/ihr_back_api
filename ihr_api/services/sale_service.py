from ihr_api import models
import string, random


def make_sale(cart, address, payment_method: int, indications, user: models.User):
    payment_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    payments = models.Payment.objects.create(
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
        payment=payments
    )


def payment_successful(payment_reference) -> bool:
    payment = models.Payment.objects.get(reference=payment_reference)
    sale = payment.sale_set.first()
    if sale.status == models.Sale.SALE_PENDING_PAYMENT and sale.payment.status == models.Payment.STATUS_PENDING:
        sale.payment.status = models.Payment.STATUS_CONFIRMED
        sale.payment.save()

        sale.status = models.Sale.SALE_CONFIRMED
        sale.save()
        return True
    return False
