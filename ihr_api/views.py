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
    serializer_class = client_serializers.ClientCategorySerializer
    permission_classes = []
    authentication_classes = []
