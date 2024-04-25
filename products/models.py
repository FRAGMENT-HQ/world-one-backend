from django.db import models
from django.utils.translation import gettext_lazy as _
from Backend.utils.constants import ActionConstants, OrderStatusConstants

# Create your models here.
class Forex(models.Model):
    currency = models.CharField(max_length=100)
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
     
        verbose_name = 'Forex'
        verbose_name_plural = 'Forex'
class Order(models.Model):
    order_id = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    amount = models.FloatField()
    forex_rate = models.FloatField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'