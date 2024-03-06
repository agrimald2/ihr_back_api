from rest_framework import serializers
from ihr_api import models


class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class AdminSubcategorySerializer(serializers.ModelSerializer):
    category = AdminCategorySerializer(many=False, read_only=True)

    class Meta:
        model = models.Subcategory
        fields = '__all__'


class AdminStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'


class AdminProductSerializer(serializers.ModelSerializer):
    subcategory = AdminSubcategorySerializer(many=False, read_only=True)
    store = AdminStoreSerializer(many=False, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'
