# Generated by Django 5.0.2 on 2024-02-23 23:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihr_api', '0004_alter_product_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=10, unique=True)),
                ('amount', models.FloatField(default=0)),
                ('payment_method', models.PositiveSmallIntegerField(choices=[(0, 'Card'), (1, 'Crypto')], default=0)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Confirmed')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=10, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sub_total', models.FloatField(default=0)),
                ('address', models.TextField(default='')),
                ('indications', models.TextField(default='')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Pending Payment'), (1, 'Confirmed'), (2, 'In Delivery'), (3, 'Delivered'), (4, 'Canceled')], default=0)),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ihr_api.payment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ihr_api.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ihr_api.sale')),
            ],
        ),
    ]
