from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .api import MethodType


METHOD_TYPE_CHOICES = [(x.value, _(x.name)) for x in MethodType]


# Create your models here.
class AbstractPayment(models.Model):
    easypay_id = models.CharField(_('Easypay ID'), max_length=100, unique=True)
    merchant_key = models.CharField(_('Merchant Key'), max_length=100, blank=True)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=100)
    method_type = models.CharField(_('Method Type'), max_length=10, choices=METHOD_TYPE_CHOICES, blank=True)
    customer_id = models.CharField(_('Customer ID'), max_length=100, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='easypay_payments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('easypay payment')
        verbose_name_plural = _('easypay payments')
        abstract = True

    def __str__(self):
        return self.easypay_id

    @classmethod
    def create(cls, merchant_key, value, payment_response, user):
        return cls(easypay_id=payment_response.id,
                   merchant_key=merchant_key,
                   amount=value,
                   status=payment_response.method.status,
                   method_type=payment_response.method.method_type.value,
                   customer_id=payment_response.customer_id,
                   user=user)
