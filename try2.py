import requests

res = requests.get("https://ibrlive.com/wp-json/my-forex-api/v1/rates?token=0097406b8fdff60c8959f03019d673d5")
res = res.json()
print(res.keys())
print(type(res["data"]))
