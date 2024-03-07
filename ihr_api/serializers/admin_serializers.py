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
    subcategory_id = serializers.IntegerField(write_only=True)
    store_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        subcategory_id = validated_data.get('subcategory_id')
        subcategory = models.Subcategory.objects.get(pk=subcategory_id)

        product = models.Product.objects.create(
            category_id=subcategory.category_id,
            **validated_data
        )

        return product

    def update(self, instance, validated_data):
        store_id = validated_data.get('store_id')
        subcategory_id = validated_data.get('subcategory_id')
        subcategory = models.Subcategory.objects.get(pk=subcategory_id)
        instance.store_id = store_id
        instance.subcategory_id = subcategory_id
        instance.category_id = subcategory.category_id
        return super().update(instance, validated_data)
