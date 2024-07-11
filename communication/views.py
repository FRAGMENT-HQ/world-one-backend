from django.shortcuts import render

# Create your views here.
from . import mail_servers

def index(request):
    x = mail_servers["tech"]
    print(x)
    return render(request, 'communication/index.html')