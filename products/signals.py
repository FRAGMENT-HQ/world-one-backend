from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def order_save(sender, instance, **kwargs):
    print("Order Save Signal",kwargs)
    # trigger if order is created
    # if kwargs.get('created', False):
    #     items = instance.order_items.all()
    #     total_amount = 0
    #     for item in items:
    #         print(item,item.inr_amount)
    #         total_amount += item.inr_amount
    #     print(total_amount)
    #     instance.amount = total_amount
    #     instance.save()
   
    # items = instance.order_items.all()
    # total_amount = 0
    # for item in items:
    #     total_amount += item.inr_amount
    # instance.amount = total_amount
    # instance.save()
