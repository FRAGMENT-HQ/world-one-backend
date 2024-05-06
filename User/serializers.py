from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name',  'phone_no', 'email', 'is_staff', 'is_superuser', 'updated_at']

class UserSignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=40)
    
    phone_no = serializers.CharField(max_length=10, required=False, allow_blank=True)
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(write_only=True)
    year = serializers.IntegerField(required=False)
    pan_card = serializers.CharField(max_length=10, required=False)
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField( required=False)
    password = serializers.CharField(write_only=True)
    phone_no = serializers.CharField(max_length=10, required=False)

