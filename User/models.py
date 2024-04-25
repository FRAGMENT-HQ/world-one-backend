from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from User.manager import UserManager
from Backend.utils.mixins import TimeStampMixin
class User(AbstractUser):
    # Some rules adding username

    group_choices = [ 
        ("a","A"),
        ("b","B")
     ]
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=10, blank=True,unique=True)
    email = models.EmailField(_('email'), max_length=80, unique=True)
    group = models.CharField(max_length=2, choices=group_choices,default="a")
    rating = models.PositiveIntegerField(default=800)
    username = None
    # Field for login
    USERNAME_FIELD = 'phone_no'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    updated_at = models.DateTimeField(auto_now=True)

    # Field for command createsuperuser
    REQUIRED_FIELDS = ['first_name','last_name','email']
    objects = UserManager()
    def __str__(self):
        return f"{self.email}"
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")



