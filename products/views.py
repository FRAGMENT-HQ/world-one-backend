from rest_framework.response import Response
from rest_framework import viewsets
from .models import Forex, Order, Visa, Ticket, Passport
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.decorators import action
from .serializers import ForexSerializer, OrderSerializer, VisaSerializer, TicketSerializer, PassportSerializer
from User.serializers import UserSignupSerializer
from User.models import User
import json
import requests
# Create your views here.

class ForexViewSet(viewsets.ModelViewSet):
    queryset = Forex.objects.all()
    serializer_class = ForexSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @action(detail=False, methods=['get'], serializer_class=VisaSerializer)
    def get_rate(self, request, *args, **kwargs):

        curr = request.GET.get('curr', None) 
        resp = requests.get(f'https://v6.exchangerate-api.com/v6/524e3784777a25a786283a89/latest/INR')
        data = resp.json()
        cr = data['conversion_rates']

        # forex = Forex.objects.filter(currency=curr).first()
        rate = cr[curr]
        for i in cr:
            forex = Forex.objects.filter(currency=i).first()
            if forex:
                forex.rate = cr[i]
                forex.save()
            else:
                forex = Forex(currency=i, rate=cr[i])
                forex.save()

        return Response(data={'rate': rate}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], serializer_class=VisaSerializer)
    def get_mini_list(self, request, *args, **kwargs):

        curr = request.GET.get('curr', None) 
        resp = requests.get(f'https://v6.exchangerate-api.com/v6/6ea75b8d7b7bc5a29831df19/latest/{curr}')
        data = resp.json()
        print(data)
        cr = data['conversion_rates']

        # forex = Forex.objects.filter(currency=curr).first()
        rate = round(cr["INR"],2)
        for i in cr:
            forex = Forex.objects.filter(currency=i).first()
            if forex:
                forex.rate = cr[i]
                forex.save()
            else:
                forex = Forex(currency=i, rate=cr[i])
                forex.save()

        return Response(data={'rate': rate}, status=status.HTTP_200_OK)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['user'] = user.pk
        serilizer = OrderSerializer(data=data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        
        return Response(data=serilizer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], serializer_class=OrderSerializer)
    def create_order(self, request, *args, **kwargs):
        data = request.data
        user= json.loads(data["user"])
        print(type(user)    )
        if User.objects.filter(phone_no=user['phone_no']).exists():
            user = User.objects.filter(phone_no=user['phone_no']).first()
        else:
            
            user["password"] = "123456"
            user_serilizer = UserSignupSerializer(data=user)
            user_serilizer.is_valid(raise_exception=True)
            user=user_serilizer.save()
        order = json.loads(data['order'])
        order['user'] = user.pk
        order_serilizer = OrderSerializer(data=order)
        order_serilizer.is_valid(raise_exception=True)
        order=order_serilizer.save()
        
        files = request.FILES
        visa_file = files.get('visa', None)
        ticket_file = files.get('ticket', None)
        passport_back_file = files.get('passport_back', None)
        passport_front_file = files.get('passport_front', None)
        if visa_file:
            visa = Visa(order=order,file=visa_file)
            visa.save()
        if ticket_file:
            ticket = Ticket(order=order_serilizer.instance)
            ticket.file = ticket_file
            ticket.save()
        if passport_back_file and passport_front_file:
            passport = Passport(order=order_serilizer.instance)
            passport.file_back = passport_back_file
            passport.file_front = passport_front_file
            passport.save()


        return Response(status=status.HTTP_201_CREATED)
class FileStorageViewSet(viewsets.ModelViewSet):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer

    @action(detail=False, methods=['post'], serializer_class=VisaSerializer)
    def visa(self, request, *args, **kwargs):
        data = request.data
        serilizer = VisaSerializer(data=data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response(data=serilizer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=TicketSerializer)
    def ticket(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], serializer_class=PassportSerializer)
    def passport(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)