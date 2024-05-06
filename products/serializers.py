from .models import Forex, Order, Visa, Ticket, Passport
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
    