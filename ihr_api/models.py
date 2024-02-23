from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class Currency(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    symbol = models.CharField(max_length=5, null=False, blank=False)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    code = models.CharField(max_length=5, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    commission = models.FloatField(null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ManyToManyField(Country, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_ADMIN = 0
    ROLE_STORE_ADMIN = 1
    ROLE_CLIENT = 2

    Roles = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STORE_ADMIN, 'Store Admin'),
        (ROLE_CLIENT, 'Client'),
    )

    role = models.IntegerField(null=False, choices=Roles, default=ROLE_CLIENT, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    hex_code = models.CharField(max_length=7, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_FEMALE = 0
    GENDER_MALE = 1
    GENDER_ANY = 2

    GENDERS = (
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
        (GENDER_ANY, 'Any'),
    )

    name = models.CharField(max_length=150, null=False, blank=False)
    name_ua = models.CharField(max_length=150, null=True, blank=True)
    name_sp = models.CharField(max_length=150, null=True, blank=True)
    name_fr = models.CharField(max_length=150, null=True, blank=True)
    name_ch = models.CharField(max_length=150, null=True, blank=True)
    code = models.CharField(max_length=150, null=False, blank=False)
    brand = models.CharField(max_length=150, null=True, blank=True)
    gender = models.IntegerField(null=True, choices=GENDERS, default=GENDER_ANY, blank=True)
    composition = models.CharField(max_length=150, null=True, blank=True)
    manufacturer = models.CharField(max_length=150, null=True, blank=True, default="China")
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    color = models.ManyToManyField(Color, blank=True)
    size = models.ManyToManyField(Size, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    METHOD_CARD = 0
    METHOD_CRYPTO = 1

    PAYMENT_METHODS = (
        (METHOD_CARD, 'Card'),
        (METHOD_CRYPTO, 'Crypto'),
    )

    STATUS_PENDING = 0
    STATUS_CONFIRMED = 1

    PAYMENT_STATUS = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
    )

    reference = models.CharField(max_length=10, unique=True, null=False, blank=False)
    amount = models.FloatField(default=0, null=False)
    payment_method = models.PositiveSmallIntegerField(default=METHOD_CARD, null=False, blank=False, choices=PAYMENT_METHODS)
    status = models.PositiveSmallIntegerField(default=STATUS_PENDING, null=False, blank=False, choices=PAYMENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference


class Sale(models.Model):
    SALE_PENDING_PAYMENT = 0
    SALE_CONFIRMED = 1
    SALE_IN_DELIVERY = 2
    SALE_DELIVERED = 3
    SALE_CANCELED = 4

    SALE_STATUS = (
        (SALE_PENDING_PAYMENT, 'Pending Payment'),
        (SALE_CONFIRMED, 'Confirmed'),
        (SALE_IN_DELIVERY, 'In Delivery'),
        (SALE_DELIVERED, 'Delivered'),
        (SALE_CANCELED, 'Canceled'),
    )

    reference = models.CharField(max_length=10, unique=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    sub_total = models.FloatField(default=0, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.TextField(default="")
    indications = models.TextField(default="")
    status = models.PositiveSmallIntegerField(default=SALE_PENDING_PAYMENT, null=False, blank=False, choices=SALE_STATUS)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
