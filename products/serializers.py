from .models import Forex, Order, Visa, Ticket, Passport,UserQuery,Pan,ExtraDocument,Resume,Outlets,OrderItems,DelievryAdress,TravelerDetails,City
from rest_framework import serializers
from User.serializers import UserSerializer
from Backend.utils.constants import ActionConstants, OrderStatusConstants, CurrencyConstanats

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forex
        fields = '__all__'

class DelievryAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelievryAdress
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class VisaSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Visa
        fields = '__all__'
class TicketSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'
class PassportSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Passport
        fields = '__all__'
    
class UserQuerySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserQuery
        fields = '__all__'
class PanSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = Pan
        fields = '__all__'
class ExtraDocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExtraDocument
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
        # status = serializers.SerializerMethodField(read_only=True)

        # def get_status(self, obj):
        #     return OrderStatusConstants.orderStatusMap[obj.status]
        class Meta:
            model = OrderItems
            fields = '__all__'
class OrderItemsListSerializer(serializers.ModelSerializer):
        status = serializers.SerializerMethodField()
        date = serializers.SerializerMethodField()
        time = serializers.SerializerMethodField()
        city = serializers.SerializerMethodField()

        def get_status(self, obj):
            return obj.order.status
        def get_date(self, obj):
            date_obj = obj.order.created_at.date()
            # format May 22, 2021
            return date_obj.strftime("%B %d, %Y")
        def get_time(self, obj):
            time_obj = obj.order.created_at.time()
            # format 12:00
            return time_obj.strftime("%H:%M")
        def get_city(self, obj):
            return obj.order.city
        class Meta:
            model = OrderItems
            fields = '__all__'
            

class OutletsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Outlets
        fields = '__all__'

class TravelerDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TravelerDetails
        fields = '__all__'