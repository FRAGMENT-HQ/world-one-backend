from .views import BlogList,BlogDetail
from django.urls import path

urlpatterns = [
    path('', BlogList.as_view(), name='blogs'),
    path('<int:blog_id>/', BlogDetail.as_view(), name='blog_detail'),
]