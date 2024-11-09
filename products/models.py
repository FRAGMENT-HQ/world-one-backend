from django.db import models
from django.utils.translation import gettext_lazy as _
from Backend.utils.constants import ActionConstants, OrderStatusConstants, CurrencyConstanats,CityConstants

from User.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.


class Forex(models.Model):
    currency = models.CharField(max_length=4, default="USD")
    rate = models.FloatField()
    markupPercentage = models.FloatField(default=0.1)
    markdownPercentage = models.FloatField(default=0.1)
    cardMarkupPercentage = models.FloatField(default=0)
    cardMarkdownPercentage = models.FloatField(default=0)
    can_buy = models.BooleanField(default=False)
    can_transfer = models.BooleanField(default=False)
    priority = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.currency}"

    class Meta:

        verbose_name = 'Forex'
        verbose_name_plural = 'Forex'

@receiver(pre_save, sender=Forex)
def set_can_transfer(sender, instance, **kwargs):
    if instance._state.adding and instance.can_transfer is False:
      
        instance.can_transfer = instance.can_buy
class Order(models.Model):
    currency = models.CharField(max_length=4, default="USD")
    action = models.IntegerField(
        choices=ActionConstants.actionChoices, default=ActionConstants.Buy)
    status = models.IntegerField(
        choices=OrderStatusConstants.orderStatusChoices, default=OrderStatusConstants.Pending)
    city = models.CharField( choices=CityConstants.CityChoices ,max_length=40, blank=True, null=True)
    amount = models.FloatField()
    total_amount = models.FloatField()
    amount_paid = models.FloatField(default=0)
    purpose_of_visit = models.CharField(max_length=40, blank=True, null=True)
    citizenship = models.CharField(max_length=40, blank=True, null=True)
    gst_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'

    def __str__(self):
        # mapper =
        # print(OrderStatusConstants.orderStatusMap[self.status])
        sta = OrderStatusConstants.orderStatusMap[self.status]
        return f"{self.user.email} {sta}"

class TravelerDetails(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='traveler_details')
    country_code = models.CharField(max_length=5, default="91")
    email = models.EmailField()
    name = models.CharField(max_length=40)
    panNumber = models.CharField(max_length=12,blank=True,null=True,default="")
    phone_no = models.CharField(max_length=14)


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.CharField(max_length=40)
    forex_amount = models.FloatField()
    inr_amount = models.FloatField()
    forex_rate = models.FloatField()
    currency = models.CharField(max_length=4, default="USD")
    bs = models.CharField(max_length=4, default="Buy")

    class Meta:
        verbose_name = 'OrderItems'
        verbose_name_plural = 'OrderItems'
    
    


class Visa(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='visa')
    file = models.FileField(upload_to='visa/', null=True, blank=True)

    class Meta:
        verbose_name = 'Visa'
        verbose_name_plural = 'Visa'


class Ticket(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='ticket')
    file = models.FileField(upload_to='ticket/', null=True, blank=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Passport(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='passport')
    file_back = models.FileField(
        upload_to='passport/back/', null=True, blank=True)
    file_front = models.FileField(
        upload_to='passport/front/', null=True, blank=True)

    class Meta:
        verbose_name = 'Passport'
        verbose_name_plural = 'Passport'


class Pan(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='pan')
    file = models.FileField(upload_to='pan/', null=True, blank=True)
    type = models.CharField(max_length=40, default="User")

    class Meta:
        verbose_name = 'Pan'
        verbose_name_plural = 'Pan'


class ExtraDocument(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='extra_document')
    file = models.FileField(upload_to='extra_document/', null=True, blank=True)
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = 'ExtraDocument'
        verbose_name_plural = 'ExtraDocument'


class DelievryAdress(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='delievry_adress')
    address = models.TextField()
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    landmark = models.CharField(max_length=40, default="")
    pincode = models.CharField(max_length=6, default="")
    phone_no = models.CharField(max_length=14)
    country_code = models.CharField(max_length=5, default="91")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DelievryAdress'
        verbose_name_plural = 'DelievryAdress'


class UserQuery(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_no = models.CharField(max_length=14)
    query = models.TextField(default="", blank=True, null=True)
    company = models.CharField(
        max_length=40, default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Resume(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='resume')
    file = models.FileField(upload_to='resume/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resume'


class Outlets(models.Model):
    icon = models.ImageField(upload_to='outlets/', null=True, blank=True)
    name = models.CharField(max_length=40)
    address = models.TextField()
    city = models.CharField(max_length=40)
    phone_no = models.CharField(max_length=14)
    email = models.EmailField()
    timming_weekdays = models.CharField(max_length=40)
    timming_weekend = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outlets'
        verbose_name_plural = 'Outlets'
    
    def __str__(self):
        return f"{self.name} {self.city}"

class City(models.Model):
    name = models.CharField(max_length=40,choices=CityConstants.CityChoices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    markup_percentage = models.FloatField(default=0.1)
    markdown_percentage = models.FloatField(default=0.1)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'City'
    
    def __str__(self):
        return f"{self.name}"
   