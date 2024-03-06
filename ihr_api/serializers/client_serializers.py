from rest_framework import serializers
from ihr_api import models


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ClientSubcategorySerializer(serializers.ModelSerializer):
    category = ClientCategorySerializer(many=False, read_only=True)

    class Meta:
        model = models.Subcategory
        fields = '__all__'


class ClientStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['id', 'name']


class ClientProductSerializer(serializers.ModelSerializer):
    subcategory = ClientSubcategorySerializer(many=False, read_only=True)
    store = ClientStoreSerializer(many=False, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'
