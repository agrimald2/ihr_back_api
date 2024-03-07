import django_filters
from ihr_api import models


class ProductFilter(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(choices=models.Product.GENDERS)
    name = django_filters.CharFilter(lookup_expr='icontains')
    size__name = django_filters.ModelChoiceFilter(queryset=models.Size.objects.all())
    color__name = django_filters.ModelChoiceFilter(queryset=models.Color.objects.all())
    subcategory = django_filters.ModelChoiceFilter(queryset=models.Subcategory.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=models.Category.objects.all())

    class Meta:
        model = models.Product
        fields = ['gender', 'name', 'size', 'color', 'subcategory', 'category']


class SaleFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=models.Sale.SALE_STATUS)
    reference = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Sale
        fields = ['status', 'reference']


class PaymentFilter(django_filters.FilterSet):
    payment_method = django_filters.ChoiceFilter(choices=models.Payment.PAYMENT_METHODS)
    reference = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=models.Payment.PAYMENT_STATUS)
    created_at = django_filters.DateFilter('created_at__date')

    class Meta:
        model = models.Payment
        fields = ['payment_method', 'reference', 'status', 'created_at']
