# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-09 10:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_order_language_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverygroup',
            name='shipping_price',
            field=django_prices.models.PriceField(currency='KES', decimal_places=4, default=0, editable=False, max_digits=12, verbose_name='shipping price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='userprofile.Address', verbose_name='billing address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_amount',
            field=django_prices.models.PriceField(blank=True, currency='KES', decimal_places=2, max_digits=12, null=True, verbose_name='discount amount'),
        ),
        migrations.AlterField(
            model_name='order',
            name='token',
            field=models.CharField(max_length=36, null=True, verbose_name='token'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_net',
            field=django_prices.models.PriceField(blank=True, currency='KES', decimal_places=2, max_digits=12, null=True, verbose_name='total net'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_tax',
            field=django_prices.models.PriceField(blank=True, currency='KES', decimal_places=2, max_digits=12, null=True, verbose_name='total tax'),
        ),
        migrations.AlterField(
            model_name='ordernote',
            name='content',
            field=models.CharField(max_length=250, verbose_name='content'),
        ),
    ]