rom __future__ import unicode_literals

from decimal import Decimal
from uuid import uuid4

import emailit.api
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import pgettext_lazy
from django_prices.models import PriceField
from payments import PaymentStatus, PurchasedItem
from payments.models import BasePayment
from prices import Price, FixedDiscount
from satchless.item import ItemLine, ItemSet

from ..discount.models import Voucher
from ..product.models import Product
from ..userprofile.models import Address

from . import OrderStatus

@python_2_unicode_compatible
class Sale(models.Model, ItemSet, index.Indexed):
    status = models.CharField(
        pgettext_lazy('Order field', 'order status'),
        max_length=32, choices=OrderStatus.CHOICES, default=OrderStatus.NEW)
    created = models.DateTimeField(
        pgettext_lazy('Order field', 'created'),
        default=now, editable=False)
    last_status_change = models.DateTimeField(
        pgettext_lazy('Order field', 'last status change'),
        default=now, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='orders',
        verbose_name=pgettext_lazy('Order field', 'user'))
    language_code = models.CharField(max_length=35, default=settings.LANGUAGE_CODE)
    tracking_client_id = models.CharField(
        pgettext_lazy('Order field', 'tracking client id'),
        max_length=36, blank=True, editable=False)
    billing_address = models.ForeignKey(
        Address, related_name='+', editable=False,blank=True, null=True,
        verbose_name=pgettext_lazy('Order field', 'billing address'))
    user_email = models.EmailField(
        pgettext_lazy('Order field', 'user email'),
        blank=True, default='', editable=False)
    token = models.CharField(
        pgettext_lazy('Order field', 'token'), null=True, max_length=36,)
    total_net = PriceField(
        pgettext_lazy('Order field', 'total net'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        blank=True, null=True)
    total_tax = PriceField(
        pgettext_lazy('Order field', 'total tax'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        blank=True, null=True)
    voucher = models.ForeignKey(
        Voucher, null=True, related_name='+', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Order field', 'voucher'))
    discount_amount = PriceField(
        verbose_name=pgettext_lazy('Order field', 'discount amount'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        blank=True, null=True)
    discount_name = models.CharField(
        verbose_name=pgettext_lazy('Order field', 'discount name'),
        max_length=255, default='', blank=True)
    class Meta:
        ordering = ('-last_status_change',)
        verbose_name = pgettext_lazy('Order model', 'Order')
        verbose_name_plural = pgettext_lazy('Order model', 'Orders')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid4())
        return super(Order, self).save(*args, **kwargs)

    def change_status(self, status):
        if status != self.status:
            self.status = status
            self.save()

