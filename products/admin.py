from django.contrib import admin
from .models import Forex, Order, Visa, Ticket, Passport,UserQuery

admin.site.register(Forex)
admin.site.register(Order)
admin.site.register(Visa)
admin.site.register(Ticket)
admin.site.register(Passport)
admin.site.register(UserQuery)


# Register your models here.
