from django.contrib import admin
from .models import Forex, Order, Visa, Ticket, Passport, UserQuery, Pan, ExtraDocument, Outlets, OrderItems, DelievryAdress, User,City
from payments.models import Payment


admin.site.site_header = "Admin"


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


class VisaInline(admin.TabularInline):
    model = Visa
    extra = 0


class TicketInline(admin.TabularInline):

    model = Ticket
    extra = 0


class PassportInline(admin.TabularInline):
    model = Passport
    extra = 0


class PanInline(admin.TabularInline):
    model = Pan
    extra = 0


class ExtraDocumentInline(admin.TabularInline):
    model = ExtraDocument
    extra = 0


class DelievryAdressInline(admin.TabularInline):
    model = DelievryAdress
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'city', 'created_at']
    list_filter = ['status', 'created_at', 'city']
    search_fields = ['user__email', 'user__name', 'user__phone_no']
    list_display_links = ['user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.city == 'ALL':
            return qs
        return qs.filter(city=request.user.city)
    inlines = [
        OrderItemsInline,
        VisaInline,
        TicketInline,
        PassportInline,
        PanInline,
        ExtraDocumentInline,
        DelievryAdressInline,
        PaymentInline,

    ]

    class Meta:
        model = Order


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_no', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone_no']

    class Meta:
        model = UserQuery

class cityAdmin(admin.ModelAdmin):
    list_display = ['name', 'markup_percentage','markdown_percentage', 'created_at']
    list_filter = ['name','created_at']
    search_fields = ['name',]

    class Meta:
        model = City

admin.site.register(Forex)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Visa)
# admin.site.register(Ticket)
# admin.site.register(Passport)
admin.site.register(UserQuery, UserQueryAdmin)
# admin.site.register(Pan)
admin.site.register(ExtraDocument)
admin.site.register(Outlets)
admin.site.register(City,cityAdmin)



# Register your models here.
