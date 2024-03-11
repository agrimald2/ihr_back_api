from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ihr_api.serializers import admin_serializers, client_serializers, shared_serializers
from ihr_api import models
from ihr_api.filters import filters
from ihr_api.services import sale_service, openpay_service, mercadopago_service
from rest_framework import viewsets, permissions
import django_filters


class APITokenObtainPairView(TokenObtainPairView):
    serializer_class = shared_serializers.APITokenObtainPairSerializer


class CreateUserView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = shared_serializers.UserSerializer
    authentication_classes = []


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = admin_serializers.AdminProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    permission_classes = []
    authentication_classes = []


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = shared_serializers.CategorySerializer
    permission_classes = []
    authentication_classes = []


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Subcategory.objects.all()
    serializer_class = shared_serializers.SubcategorySerializer
    permission_classes = []
    authentication_classes = []


class CountryViewSet(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = shared_serializers.CountrySerializer
    permission_classes = []
    authentication_classes = []


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = models.Currency.objects.all()
    serializer_class = shared_serializers.CurrencySerializer
    permission_classes = []
    authentication_classes = []


class StoreViewSet(viewsets.ModelViewSet):
    queryset = models.Store.objects.all()
    serializer_class = admin_serializers.AdminStoreSerializer
    permission_classes = []
    authentication_classes = []


class SaleViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = shared_serializers.SaleSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.SaleFilter
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        cart, cart_total, shipping_info, payment_method, billing_info = sale_service.process_request(request)
        if cart is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid cart data'})
        if payment_method is None or payment_method > 4:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid payment method'})
        if shipping_info is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid shipping data'})
        payment_reference, sale_reference = sale_service.make_sale(cart, cart_total, shipping_info, payment_method, billing_info, None)
        return Response(status=status.HTTP_200_OK, data={'payment_reference': payment_reference, 'sale_reference': sale_reference})


class BillingAccountViewSet(viewsets.ModelViewSet):
    queryset = models.BillingAccount.objects.all()
    serializer_class = shared_serializers.BillingAccountSerializer
    permission_classes = []
    authentication_classes = []
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.BillingAccountFilter


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = shared_serializers.PaymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filters.PaymentFilter
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        sale_reference = data.get('sale_reference', None)
        payment_method = data.get('payment_method', None)

        sale = models.Sale.objects.get(reference=sale_reference)
        payment_success = False

        if payment_method == models.Payment.METHOD_OPEN_PAY or payment_method == models.Payment.METHOD_MERCADOPAGO:
            source_id = mercadopago_service.generate_token(data)
            print(source_id)
            payment_success = mercadopago_service.create_payment(source_id, sale)
        elif payment_method == models.Payment.METHOD_CRYPTO:
            payment_success = False
        elif payment_method == models.Payment.METHOD_APPLE_PAY:
            payment_success = False

        if payment_success:
            payment = sale.payment
            payment.status = models.Payment.STATUS_CONFIRMED
            payment.save()

            sale.status = models.Sale.SALE_CONFIRMED
            sale.save()

        if payment_success:
            return Response(status=status.HTTP_200_OK, data={'message': 'Payment successful'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Payment failed'})
