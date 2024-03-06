from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from ihr_api.serializers import admin_serializers, client_serializers, shared_serializers
from ihr_api import models
from ihr_api.filters import filters
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
    permission_classes = []
    authentication_classes = []


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = shared_serializers.PaymentSerializer
    permission_classes = []
    authentication_classes = []
