# Generated by Django 5.0.2 on 2024-03-11 01:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihr_api', '0011_billingaccount_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='billing_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ihr_api.billingaccount'),
        ),
    ]
