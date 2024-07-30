from django.urls import path, include, re_path

from payments.views import webhook
urlpatterns = [
    
    path('payment', webhook.as_view()),
    
]
