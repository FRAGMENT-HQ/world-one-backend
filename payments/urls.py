from .views import PayoutsView
from django.urls import path

urlpatterns = [
    path('payouts/', PayoutsView.as_view(), name='payouts'),
]