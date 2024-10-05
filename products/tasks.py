
from .models import Forex
import requests

def update_database():
    respose =requests.get("https://ibrlive.com/wp-json/my-forex-api/v1/rates?token=0097406b8fdff60c8959f03019d673d5")
    respose = respose.json()
    respose = respose["data"]
    print("I work")
    for data in respose:
        if data["from_curr"] == "INR":
            forObj = Forex.objects.filter(currency=data["to_curr"])
            if forObj.exists():
                forObj=forObj[0]
                forObj.rate = data["rate"]
                forObj.save()
            else:
                forObj = Forex.objects.create(
                    currency = data["to_curr"],
                    rate = data["rate"]

                   
                )
                # forObj.save()



    print("updating ...")
