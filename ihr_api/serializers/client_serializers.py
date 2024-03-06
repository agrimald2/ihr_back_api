from rest_framework import serializers
from ihr_api import models
from ihr_api.serializers import shared_serializers


class ClientStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['id', 'name']


class ClientProductSerializer(serializers.ModelSerializer):
    subcategory = shared_serializers.SubcategorySerializer(many=False, read_only=True)
    store = ClientStoreSerializer(many=False, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'
