from django.urls import path, include, re_path
from User import urls as user_urls
from products import urls as product_urls
from blogs import urls as blog_urls
from products.views import OutletsView,ItemsViewSet,ResumeViewSet,AddAdressView,CityRates
from payments import urls as paymenturls
urlpatterns = [
    path('users/', include(user_urls)),
    path('products/', include(product_urls)),
    path('outlets/', OutletsView.as_view()),
    path('items/', ItemsViewSet.as_view()),
    path('resume/', ResumeViewSet.as_view()),
    path('add-adress/', AddAdressView.as_view()),
    path('payments/', include(paymenturls)),
    path('blogs/', include(blog_urls)),
    path('city-rates/', CityRates.as_view())
]
