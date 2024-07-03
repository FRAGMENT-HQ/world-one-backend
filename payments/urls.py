from .views import PayoutsView,confirmation
from django.urls import path

urlpatterns = [
    path('payouts/', PayoutsView.as_view(), name='payouts'),
    path('confirmation/', confirmation.as_view(), name='confirmation')
]