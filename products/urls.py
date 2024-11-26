from .views import ForexViewSet,OrderViewSet,FileStorageViewSet,UserQueryViewSet, CityRates
from rest_framework.routers import DefaultRouter
from .models import City
from Backend.utils.constants import CityConstants
from django.core.exceptions import ObjectDoesNotExist
from .models import Forex
# from multiprocessing import Process, Queue, Pool, Manager, Lock, Semaphore
from threading import Thread
import requests
import time

def update_forex():
    respose =requests.get("https://ibrlive.com/wp-json/my-forex-api/v1/rates?token=0097406b8fdff60c8959f03019d673d5")
    respose = respose.json()
    respose = respose["data"]
    
    for data in respose:
        if data["from_curr"] == "INR":
            forObj = Forex.objects.filter(currency=data["to_curr"])
            if forObj.exists():
                forObj=forObj[0]
                forObj.rate = data["rate"]
                forObj.save()
            else:
                forObj = Forex.objects.create(
                    
                        currency=data["to_curr"],
                        rate=data["rate"]

                    
                )



def crete_city(city_name):
    try:
        city = City.objects.get(name=city_name)
    except ObjectDoesNotExist:
        city = City.objects.create(name=city_name)
  
        city.save()
        print(f"{city_name} is created")

for city in CityConstants.CityChoices:
    crete_city(city[1])



# run update_forex() in a separate process every three minutes
def run_update_forex():
    while True:
        update_forex()
        time.sleep(60)
# run_update_forex()in a separate process
thread = Thread(target=run_update_forex)
thread.daemon = True  # Ensure the thread stops when the main program exits
thread.start()





router = DefaultRouter()
router.register(r'forex', ForexViewSet, basename='forex')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'filestorage', FileStorageViewSet, basename='filestorage'),
router.register(r'userquery', UserQueryViewSet, basename='userquery')



urlpatterns = router.urls+[
    
]
