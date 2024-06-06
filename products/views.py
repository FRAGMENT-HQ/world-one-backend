from rest_framework.response import Response
from rest_framework import viewsets
from .models import Forex, Order, Visa, Ticket, Passport, UserQuery, Pan, ExtraDocument, Resume, Outlets, OrderItems
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from .serializers import ForexSerializer, OrderSerializer, VisaSerializer, TicketSerializer, PassportSerializer, UserQuerySerializer, OutletsSerializer, OrderItemsSerializer,OrderItemsListSerializer
from User.serializers import UserSignupSerializer
from User.models import User
from rest_framework.generics import ListAPIView
import json

import requests
# Create your views here.


class OutletsView(ListAPIView):
    queryset = Outlets.objects.all()
    serializer_class = OutletsSerializer
    permission_classes = [AllowAny]


class ItemsViewSet(APIView):
   def get(self,request,*args,**kwargs):
        email = request.GET.get('email',None)
        order = OrderItems.objects.filter(order__user__email=email)
        serilzer = OrderItemsListSerializer(order,many=True)
        return Response(data=serilzer.data,status=status.HTTP_200_OK)
    

class ForexViewSet(viewsets.ModelViewSet):
    queryset = Forex.objects.all()
    serializer_class = ForexSerializer
    prioroity_set = ['USD', 'EUR', 'GBP', 'CAD', 'SGD', "AUD"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):

        inc_quryset = Forex.objects.all().filter(currency__in=self.prioroity_set)
        exc_quryset = Forex.objects.all().exclude(currency__in=self.prioroity_set)
        inc_quryset = sorted(inc_quryset, key=lambda x: self.prioroity_set.index(x.currency))
        queryset = list(inc_quryset) + list(exc_quryset)
        # sorted(queryset, key=lambda x: self.prioroity_set.index(x.currency))
        serializer = self.get_serializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=ForexSerializer)
    def mini(self, request, *args, **kwargs):
        queryset = list(Forex.objects.all().filter(currency__in=self.prioroity_set))
        queryset = sorted(queryset, key=lambda x: self.prioroity_set.index(x.currency),reverse=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
   


    @action(detail=False, methods=['get'], serializer_class=VisaSerializer)
    def get_rate(self, request, *args, **kwargs):

        curr = request.GET.get('curr', None)
        resp = requests.get(
            f'https://v6.exchangerate-api.com/v6/c7dbfb5bc19040987eb0a90f/latest/INR')
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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create_order',"List"] :
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], serializer_class=OrderSerializer)
    def create_order(self, request, *args, **kwargs):
        data = request.data
        user = json.loads(data["user"])
        name = data['name']
       
        if User.objects.filter(phone_no=user['phone_no']).exists():
            user = User.objects.filter(phone_no=user['phone_no']).first()
        else:

            user["password"] = "123456"
            user_serilizer = UserSignupSerializer(data=user)
            user_serilizer.is_valid(raise_exception=True)
            user = user_serilizer.save()
        order = json.loads(data['order'])
        order['user'] = user.pk
        order_serilizer = OrderSerializer(data=order)
        order_serilizer.is_valid(raise_exception=True)
        order = order_serilizer.save()

        items = json.loads(data['items'])
        for item in items:
            item['order'] = order.pk
            item_serilizer = OrderItemsSerializer(data=item)
            item_serilizer.is_valid(raise_exception=True)
            item_serilizer.save()

        files = request.FILES

        visa_file = files.get('visa', None)
        ticket_file = files.get('ticket', None)
        passport_back_file = files.get('passport_back', None)
        passport_front_file = files.get('passport_front', None)
        pan_file = data.get('pan', None)
        extra_file = files.get('extra_file', None)
        c_pan = files.get('c_pan', None)

        if visa_file:
            visa = Visa(order=order, file=visa_file)
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
        if pan_file:
            pan = Pan(order=order_serilizer.instance)
            pan.file = pan_file
            pan.save()
        if extra_file:
            extra = ExtraDocument(order=order_serilizer.instance, name=name)
            extra.file = extra_file
            extra.save()
        if c_pan:
            pan = Pan(order=order_serilizer.instance)
            pan.file = c_pan
            pan.type = "Company"
            pan.save()

        return Response(status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], serializer_class=OrderSerializer)
    def List(self,request,*args,**kwargs):
        pass
        

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


class UserQueryViewSet(viewsets.ModelViewSet):
    queryset = UserQuery.objects.all()
    serializer_class = UserQuerySerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ResumeViewSet(APIView):
    def post(self, request, *args, **kwargs):
        # data = request.data
        files = request.FILES
        res_file = files.get('resume', None)
        resume = Resume(file=res_file)
        resume.save()
        return Response(status=status.HTTP_201_CREATED)

