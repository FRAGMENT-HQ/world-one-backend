from django.contrib import admin
from .models import User

@admin.register(User)
class userAdmin( admin.ModelAdmin):
    list_display = ['email','first_name','last_name','group','phone_no']
   
