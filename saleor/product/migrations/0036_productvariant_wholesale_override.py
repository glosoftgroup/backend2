# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-06 02:56
from __future__ import unicode_literals

from django.db import migrations
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_remove_producttax_scope'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='wholesale_override',
            field=django_prices.models.PriceField(blank=True, currency='USD', decimal_places=2, max_digits=12, null=True, verbose_name='wholesale override'),
        ),
    ]