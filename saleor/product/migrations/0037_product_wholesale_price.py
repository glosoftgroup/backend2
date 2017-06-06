# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-06 05:30
from __future__ import unicode_literals

from django.db import migrations
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_productvariant_wholesale_override'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='wholesale_price',
            field=django_prices.models.PriceField(blank=True, currency='USD', decimal_places=2, max_digits=12, null=True, verbose_name='Wholesale price'),
        ),
    ]
