import http.client
from . import mail_servers
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import ssl

def send_otp(otp,name,phone,user_id):
    conn = http.client.HTTPSConnection("control.msg91.com")

    payload = payload = "{\n  \"template_id\": \"668e4c88d6fc055e9a235142\",\n  \"short_url\": \"0\",\n  \"realTimeResponse\": \"1\", \n  \"recipients\": [\n    {\n      \"mobiles\": \""+phone+"\",\n      \"code\": \""+user_id+" is \",\n      \"phone\": \""+otp+"\",\n      \"OTP\": \""+name+"\",\n      \"name\": \"veification with\"\n    }\n  ]\n}"


    headers = {
        'authkey': "",
        'accept': "application/json",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v5/flow", payload, headers)

    res = conn.getresponse()
    data = res.read()

def send_email(subject, body, to_email):
    from_email = os.getenv('FROM_EMAIL')
    from_email_password = os.getenv('FROM_EMAIL_PASSWORD')

    # Create the email object
    msg = MIMEMultipart()
    msg['From'] = "tech@worldoneforex.com"
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'html'))
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT@SECLEVEL=1')


    try:
        # Connect to the Rediffmail Pro server
        server = mail_servers["tech"]

        # Send the email
        server.send_message(msg)

        # Disconnect from the server
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")
