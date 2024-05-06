from django.db import models
from django.utils.translation import gettext_lazy as _
from Backend.utils.constants import ActionConstants, OrderStatusConstants,CurrencyConstanats


from User.models import User

# Create your models here.
class Forex(models.Model):
    currency = models.CharField(max_length=4, default="USD")
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
     
        verbose_name = 'Forex'
        verbose_name_plural = 'Forex'


class Order(models.Model):
    currency = models.CharField(max_length=4, default="USD")
    action = models.IntegerField(choices=ActionConstants.actionChoices, default=ActionConstants.Buy)
    status = models.IntegerField(choices=OrderStatusConstants.orderStatusChoices, default=OrderStatusConstants.Pending)
    amount = models.FloatField()
    forex_rate = models.FloatField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='order')
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
class Visa(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='visa')
    file = models.FileField(upload_to='visa/',null=True, blank=True)
    class Meta:
        verbose_name = 'Visa'
        verbose_name_plural = 'Visa'
class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ticket')
    file = models.FileField(upload_to='ticket/',null=True, blank=True)
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Ticket'
class Passport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='passport')
    file_back = models.FileField(upload_to='passport/back/', null=True, blank=True)
    file_front = models.FileField(upload_to='passport/front/',null=True, blank=True)
    class Meta:
        verbose_name = 'Passport'
        verbose_name_plural = 'Passport'