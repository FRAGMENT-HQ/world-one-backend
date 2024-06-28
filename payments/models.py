from django.db import models
from products.models import Order

# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_payment')
    cashfree_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    payment_request_id = models.CharField(max_length=100)
    payment_amount = models.CharField(max_length=100)