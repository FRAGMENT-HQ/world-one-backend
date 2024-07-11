import json
import smtplib
import os
import ssl

mailIds = dict(json.loads(open('mail.json').read()))
context = ssl.create_default_context()
context.set_ciphers('DEFAULT@SECLEVEL=1')

mail_servers = {}

for i in mailIds:
    print(i)
    server = smtplib.SMTP(mailIds[i]["host"], mailIds[i]["port"])
    server.starttls(context=context)
    server.login(mailIds[i]["email"], mailIds[i]["password"])
    mail_servers[i] = server
