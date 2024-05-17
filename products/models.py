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
    city = models.CharField(max_length=40, blank=True,null=True)
    amount = models.FloatField()
    forex_rate = models.FloatField()
    product = models.CharField(max_length=40, blank=True,null=True)
    total_amount = models.FloatField()
    purous_of_visit = models.CharField(max_length=40, blank=True,null=True)
    citizenship = models.CharField(max_length=40, blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='order')
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
    def __str__(self):
        # mapper = 
        # print(OrderStatusConstants.orderStatusMap[self.status])
        sta = OrderStatusConstants.orderStatusMap[self.status]
        return f"{self.user.email} {sta}"
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
class ExtraDocument(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='extra_document')
    file = models.FileField(upload_to='extra_document/',null=True, blank=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    class Meta:
        verbose_name = 'ExtraDocument'
        verbose_name_plural = 'ExtraDocument'

class UserQuery(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_no = models.CharField(max_length=12)
    query = models.TextField()
    