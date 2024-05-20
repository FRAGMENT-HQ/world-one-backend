from .models import Forex, Order, Visa, Ticket, Passport,UserQuery,Pan,ExtraDocument
from rest_framework import serializers
from User.serializers import UserSerializer
from Backend.utils.constants import ActionConstants, OrderStatusConstants, CurrencyConstanats
class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forex
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