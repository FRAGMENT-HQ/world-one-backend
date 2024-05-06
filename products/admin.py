from django.contrib import admin
from .models import Forex, Order, Visa, Ticket, Passport

admin.site.register(Forex)
admin.site.register(Order)
admin.site.register(Visa)
admin.site.register(Ticket)
admin.site.register(Passport)


# Register your models here.
