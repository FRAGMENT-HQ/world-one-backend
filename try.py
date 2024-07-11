# 80f31d2-39c6-11ef-8b60-0200cd936042

import requests
import json


# url = "https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d80f31d2-39c6-11ef-8b60-0200cd936042&to=9833290022&from=txwone&templatename=Temp1&var1=Pranav&var2=771288"
# payload = {
#     'module': 'TRANS_SMS',
#     'apikey': '80f31d2-39c6-11ef-8b60-0200cd936042',
#     'to': '919833290022,',
#     'from': 'HEADER',
#     'msg': 'DLT Approved Message Text Goes Here'
# }

# response = requests.post(url)
# print(response.text)

# send email

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import ssl

# sent sms using msg 91

import http.client

conn = http.client.HTTPSConnection("control.msg91.com")

payload = "{\n  \"template_id\": \"EntertemplateID\",\n  \"short_url\": \"1 (On) or 0 (Off)\",\n  \"realTimeResponse\": \"1 (Optional)\", \n  \"recipients\": [\n    {\n      \"mobiles\": \"919833290022\",\n      \"VAR\": \"VALUE 1\"\n    }\n  ]\n}"

headers = {
    'authkey': "42bP1",
    'accept': "application/json",
    'content-type': "application/json"
    }

conn.request("POST", "/api/v5/flow", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))



# def send_email(subject, body, to_email):
#     from_email = os.getenv('FROM_EMAIL')
#     from_email_password = os.getenv('FROM_EMAIL_PASSWORD')

#     # Create the email object
#     msg = MIMEMultipart()
#     msg['From'] = "tech@worldoneforex.com"
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     # Attach the body to the email
#     msg.attach(MIMEText(body, 'plain'))
#     context = ssl.create_default_context()
#     context.set_ciphers('DEFAULT@SECLEVEL=1')


#     try:
#         # Connect to the Rediffmail Pro server
#         server = smtplib.SMTP('smtp.rediffmailpro.com', 587)
#         server.starttls(context=context)


#         # Login to the email account
#         server.login("tech@worldoneforex.com", "admin_admin")

#         # Send the email
#         server.send_message(msg)

#         # Disconnect from the server
#         server.quit()

#         print("Email sent successfully!")

#     except Exception as e:
#         print(f"Failed to send email. Error: {e}")

# # Usage
# subject = "tech@worldoneforex.com"
# body = "This is a test email."
# to_email = "pranavleo22@gmail.com"

# send_email(subject, body, to_email)
