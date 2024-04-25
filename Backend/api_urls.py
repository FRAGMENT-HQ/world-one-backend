from django.urls import path, include, re_path
from User import urls as user_urls
urlpatterns = [
    path('users/', include(user_urls)),
]
