from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from User.manager import UserManager
from Backend.utils.constants import CityConstants


class User(AbstractUser):

    name = models.CharField(max_length=40, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, unique=True)
    country_code = models.CharField(max_length=5, blank=True)
    email = models.EmailField(_('email'), max_length=80)
    pan_card = models.CharField(max_length=10, blank=True, null=True)
    username = None
    USERNAME_FIELD = 'phone_no'
    verification_status = models.BooleanField(default=False)
    otp = models.CharField(default="",max_length=6)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(choices=CityConstants.CityChoices,
                            max_length=40, blank=True, null=True)

    # Field for command createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
