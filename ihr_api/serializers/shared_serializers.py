from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ihr_api import models
from ihr_api.serializers import client_serializers
import string
import random


class APITokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional data to the response
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser

        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        user = models.User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Subcategory
        fields = '__all__'

    def update(self, instance, validated_data):
        category_id = validated_data.get('category_id')
        instance.category_id = category_id
        return super().update(instance, validated_data)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = '__all__'


class BillingAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillingAccount
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)
    billing_account = BillingAccountSerializer(many=False, read_only=True)
    sale_reference = serializers.SerializerMethodField()

    class Meta:
        model = models.Payment
        fields = '__all__'

    def get_sale_reference(self, obj):
        sale = models.Sale.objects.filter(payment=obj).first()
        return sale.reference


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = models.SaleItem
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = models.Sale
        fields = '__all__'

    def get_items(self, obj):
        items = models.SaleItem.objects.filter(sale=obj)
        return SaleItemSerializer(items, many=True).data


class PaymentLinkSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)
    currency_id = serializers.IntegerField(write_only=True)
    billing_account = BillingAccountSerializer(many=False, read_only=True)
    billing_account_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.PaymentLink
        fields = '__all__'

    def create(self, validated_data):
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        validated_data['reference'] = reference
        currency_id = validated_data.get('currency_id')
        currency = models.Currency.objects.get(pk=currency_id)
        billing_account_id = validated_data.get('billing_account_id')
        billing_account = models.BillingAccount.objects.get(pk=billing_account_id)

        link = models.PaymentLink.objects.create(
            currency=currency,
            billing_account=billing_account,
            **validated_data
        )

        return link
