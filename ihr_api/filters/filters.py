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
