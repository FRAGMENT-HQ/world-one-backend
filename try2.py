import http.client

conn = http.client.HTTPSConnection("control.msg91.com")

payload = "{\n  \"template_id\": \"668e4c88d6fc055e9a235142\",\n  \"short_url\": \"0\",\n  \"realTimeResponse\": \"1\", \n  \"recipients\": [\n    {\n      \"mobiles\": \"919833290022\",\n      \"code\": \"9140921335 is \",\n      \"phone\": \"998866\",\n      \"OTP\": \"pranav\",\n      \"name\": \"veification with\"\n    }\n  ]\n}"

headers = {
    'authkey': "426019AjoLCxbOvSF668e382bP1",
    'accept': "application/json",
    'content-type': "application/json"
}

conn.request("POST", "/api/v5/flow", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
