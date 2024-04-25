from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from datetime import datetime,timedelta

@receiver(post_save,sender=User)
def create_user_analytics(sender,instance,created,**kwargs):
    pass


    