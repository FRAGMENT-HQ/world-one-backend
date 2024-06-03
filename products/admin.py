from django.contrib import admin
from .models import Forex, Order, Visa, Ticket, Passport,UserQuery,Pan,ExtraDocument,Outlets

admin.site.register(Forex)
admin.site.register(Order)
admin.site.register(Visa)
admin.site.register(Ticket)
admin.site.register(Passport)
admin.site.register(UserQuery)
admin.site.register(Pan)
admin.site.register(ExtraDocument)
admin.site.register(Outlets)


# Register your models here.
