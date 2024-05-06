from django.urls import path, include, re_path
from User import urls as user_urls
from products import urls as product_urls
urlpatterns = [
    path('users/', include(user_urls)),
    path('products/', include(product_urls)),
]
