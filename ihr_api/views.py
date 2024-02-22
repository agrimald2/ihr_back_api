from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from ihr_api.serializers import admin_serializers, client_serializers, shared_serializers
from ihr_api import models


class APITokenObtainPairView(TokenObtainPairView):
    serializer_class = shared_serializers.APITokenObtainPairSerializer


class CreateUserView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = shared_serializers.UserSerializer
    authentication_classes = []
