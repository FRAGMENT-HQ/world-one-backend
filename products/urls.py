from .views import ForexViewSet,OrderViewSet,FileStorageViewSet,UserQueryViewSet, CityRates
from rest_framework.routers import DefaultRouter
from .models import City
from Backend.utils.constants import CityConstants
from django.core.exceptions import ObjectDoesNotExist


def crete_city(city_name):
    try:
        city = City.objects.get(name=city_name)
    except ObjectDoesNotExist:
        city = City.objects.create(name=city_name)
  
        city.save()
        print(f"{city_name} is created")

# for city in CityConstants.CityChoices:
#     crete_city(city[1])
router = DefaultRouter()
router.register(r'forex', ForexViewSet, basename='forex')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'filestorage', FileStorageViewSet, basename='filestorage'),
router.register(r'userquery', UserQueryViewSet, basename='userquery')



urlpatterns = router.urls+[
    
]
