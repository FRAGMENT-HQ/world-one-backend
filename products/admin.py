from django.contrib import admin
from .models import Forex, Order, Visa, Ticket, Passport, UserQuery, Pan, ExtraDocument, Outlets, OrderItems, DelievryAdress, User,City,Resume
from payments.models import Payment
from .forms import CSVUploadForm
import csv
from io import TextIOWrapper
from django.shortcuts import render, redirect


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
        if request.user.city == 'all':
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

class ForexAdmin(admin.ModelAdmin):
  
    # search_fields = ['currency']

    change_list_template = "admin/products/forex_changelist.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name='upload_csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding='utf-8')
                reader = csv.reader(csv_file)
                for row in reader:
                    name = row[0]
                    obj =Forex.objects.filter(currency=name)
                    if obj.exists():
                        obj = obj.first()
                        obj.markupPercentage=row[1] 
                        obj.markdownPercentage=row[2]
                        obj.cardMarkupPercentage=row[3]
                        obj.cardMarkdownPercentage=row[4]
                        obj.save()
                    print(row)
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        form = CSVUploadForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)
    class Meta:
        model = Forex

admin.site.register(Forex,ForexAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(Outlets)
admin.site.register(City,cityAdmin)
admin.site.register(Resume)


# Register your models here.
