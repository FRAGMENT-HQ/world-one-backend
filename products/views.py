from rest_framework.response import Response
from rest_framework import viewsets
from .models import Forex, Order, Visa, Ticket, Passport, UserQuery, Pan, ExtraDocument, Resume, Outlets, OrderItems, City
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.decorators import action
from rest_framework.views import APIView
from .serializers import ForexSerializer, OrderSerializer, VisaSerializer, TicketSerializer, PassportSerializer, UserQuerySerializer, OutletsSerializer, OrderItemsSerializer, OrderItemsListSerializer, DelievryAdressSerializer, TravelerDetailsSerializer, CitySerializer
from User.serializers import UserSignupSerializer
from User.models import User
from rest_framework.generics import ListAPIView
import json
import datetime
import pytz
from communication.utils import send_email
# get django groups
from django.contrib.auth.models import Group
import requests
# Create your views here.
india_tz = pytz.timezone('Asia/Kolkata')

def update_forex():
    obj = Forex.objects.first()
    if obj:
        # convert ot indian standerd time
        # now = datetime.datetime.now( datetime.timezone.utc).astimezone(datetime.timezone.utc )
        if not obj.created_at.astimezone(india_tz) + datetime.timedelta(minutes=10) < datetime.datetime.now(india_tz):
            resp = requests.get(
            f'https://v6.exchangerate-api.com/v6/c7dbfb5bc19040987eb0a90f/latest/INR')
            try:
                data = resp.json()
                cr = data['conversion_rates']

                # forex = Forex.objects.filter(currency=curr).first()

                for i in cr:
                    print(i)
                    forex = Forex.objects.filter(currency=i).first()
                    if forex:
                        forex.rate = cr[i]
                        forex.created_at = datetime.datetime.now(india_tz)
                        forex.save()
                    else:
                        forex = Forex(currency=i, rate=cr[i])
                        forex.save()
            except:
                pass

class OutletsView(ListAPIView):
    queryset = Outlets.objects.all()
    serializer_class = OutletsSerializer
    permission_classes = [AllowAny]


class CityRates(APIView):
    def get(self, request, *args, **kwargs):
        city = request.GET.get('city', None)
        if city:
            city = City.objects.filter(name=city).first()
        else:
            city = City.objects.filter(name='all').first()

        return Response(data=CitySerializer(city).data, status=status.HTTP_200_OK)


class ItemsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        order = OrderItems.objects.filter(order__user=user.pk)
        serilzer = OrderItemsListSerializer(order, many=True)
        return Response(data=serilzer.data, status=status.HTTP_200_OK)


class AddAdressView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serilizer = DelievryAdressSerializer(data=data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response(data=serilizer.data, status=status.HTTP_201_CREATED)


class ForexViewSet(viewsets.ModelViewSet):
    queryset = Forex.objects.all()
    serializer_class = ForexSerializer
    prioroity_set = ['USD', 'EUR', 'GBP', 'CAD', 'SGD', "AUD"]

    


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ["mini", "get_rate", "list"] :
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        update_forex()
        city = request.GET.get('city', None)
        if city:
            city = City.objects.filter(name=city).first()
        else:
            city = City.objects.filter(name='all').first()

        inc_quryset = Forex.objects.all().filter(priority__gt=0).order_by('priority')
        
        
        queryset = list(inc_quryset) 
        # sorted(queryset, key=lambda x: self.prioroity_set.index(x.currency))
        serializer = self.get_serializer(queryset, many=True)

        return Response(data={"data": serializer.data, "city": CitySerializer(city).data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=ForexSerializer)
    def mini(self, request, *args, **kwargs):
        update_forex()
        queryset = list(Forex.objects.all().filter(
            currency__in=self.prioroity_set))
        queryset = sorted(queryset, key=lambda x: self.prioroity_set.index(
            x.currency), reverse=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=VisaSerializer)
    def get_rate(self, request, *args, **kwargs):
        # check if Forex had been called 10 minutes ago
        curr = request.GET.get('curr', None)
        city = request.GET.get('city', None)
        product = request.GET.get('product', "currancy")
        rate = Forex.objects.filter(currency=curr)
        if rate.exists():
            rate = rate.first()
        else:
            return Response(data={'error': 'Currency not found'}, status=status.HTTP_404_NOT_FOUND)
        mark_up = rate.markupPercentage if product == "currancy" else rate.cardMarkupPercentage
        mark_down = rate.markdownPercentage if product == "currancy" else rate.cardMarkdownPercentage

        if city:
            city = City.objects.filter(name=city).first()
        else:
            city = City.objects.filter(name='All').first()
        citySer = CitySerializer(city)

        obj = Forex.objects.first()
        usd = Forex.objects.filter(currency='USD').first()

        if obj:
            # convert ot indian standerd time
            # now = datetime.datetime.now( datetime.timezone.utc).astimezone(datetime.timezone.utc )
            if obj.created_at.astimezone(india_tz) + datetime.timedelta(minutes=10) < datetime.datetime.now(india_tz):
                print(obj.created_at + datetime.timedelta(minutes=10)
                      < datetime.datetime.now(india_tz))

                rate = Forex.objects.filter(currency=curr).first()
                

                return Response(data={'rate': rate.rate, "mark_up": mark_up, "mark_down": mark_down, "usd": usd.rate, "city": citySer.data}, status=status.HTTP_200_OK)

        resp = requests.get(
            f'https://v6.exchangerate-api.com/v6/c7dbfb5bc19040987eb0a90f/latest/INR')
        try:
            data = resp.json()
            cr = data['conversion_rates']

            # forex = Forex.objects.filter(currency=curr).first()

            for i in cr:
                print(i)
                forex = Forex.objects.filter(currency=i).first()
                if forex:
                    forex.rate = cr[i]
                    forex.created_at = datetime.datetime.now(india_tz)
                    forex.save()
                else:
                    forex = Forex(currency=i, rate=cr[i])
                    forex.save()
            usd = Forex.objects.filter(currency='USD').first()
            rate = Forex.objects.filter(currency=curr).first()

            return Response(data={'rate': rate.rate, "mark_up": mark_up, "mark_down": mark_down, "city": citySer.data, 'usd': usd.rate}, status=status.HTTP_200_OK)
        except:
            rate = Forex.objects.filter(currency=curr).first()
            usd = Forex.objects.filter(currency='USD').first()
            return Response(data={'rate': rate.rate, 'usd': usd.rate, "mark_up": mark_up, "mark_down": mark_down, "city": citySer.data}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], serializer_class=ForexSerializer)
    def get_can_buy_rate(self, request, *args, **kwargs):
        data = Forex.objects.filter(can_buy=True)
        serializer = self.get_serializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["List"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], serializer_class=OrderSerializer)
    def create_order(self, request, *args, **kwargs):
        data = request.data
        user = json.loads(data["user"])
        name = data['name']

        user = request.user

        order = json.loads(data['order'])
        order['user'] = user.pk
        order_serilizer = OrderSerializer(data=order)
        order_serilizer.is_valid(raise_exception=True)
        order = order_serilizer.save()
        print(data['user'])
        dataUser = json.loads(data['user'])
        dataUser['order'] = order.pk
        travler = TravelerDetailsSerializer(data=dataUser)
        travler.is_valid(raise_exception=True)
        # travler.save(order=order)

        try:
            items = json.loads(data['items'])
            for item in items:
                item['order'] = order.pk
                item_serilizer = OrderItemsSerializer(data=item)
                item_serilizer.is_valid(raise_exception=True)
                item_serilizer.save()
        except:
            pass

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

        return Response(status=status.HTTP_201_CREATED, data={'id': order.pk})

    @action(detail=False, methods=['post'], serializer_class=OrderSerializer)
    def List(self, request, *args, **kwargs):

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

    def create(self, request, *args, **kwargs):
        print(request.data)
        data = request.data

        admins = Group.objects.get(name='query_admin')
        # send email to all admins
        print(admins.user_set.all())
        emails = [admin.email for admin in admins.user_set.all()]
        for email in emails:
            send_email(
                subject="New Query",
                body="A new query has been submitted<br> Please check the admin panel for more details<br> by: " +
                data["name"]+"<br>email: "+data["email"]+"<br>querry: "+data["query"]+"<br>Regards, <br>WorldOne Forex",
                to_email=email
            )

        return super().create(request, *args, **kwargs)


class ResumeViewSet(APIView):
    def post(self, request, *args, **kwargs):
        # data = request.data
        files = request.FILES
        res_file = files.get('resume', None)
        resume = Resume(file=res_file)
        resume.save()
        return Response(status=status.HTTP_201_CREATED)
