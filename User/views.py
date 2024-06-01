from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import User 
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], serializer_class=UserSignupSerializer)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)

        try:
            access_token = str(refresh.access_token)
            
        except TokenError:
           
            return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = Response({'detail': 'Created Sucesfull', 'access_token': access_token, 'user' : UserSignupSerializer(user).data,  'refresh_token':str(refresh)}, status=status.HTTP_201_CREATED)
        
        # Set the refresh token as a cookie in the response
        response.set_cookie(
            key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
            value=str(refresh),
            httponly=True,
            samesite=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'],
        )
        
        return response

    @action(detail=False, methods=['post'], serializer_class=UserLoginSerializer)
    def login(self, request):
       
        data = request.data
        serializer = self.get_serializer(data=data)
        
       
        try:
            serializer.is_valid(raise_exception=True)
        
        except Exception as e:
            return Response({'error': 'Invalid credentials',"data":serializer.errors}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        user = None
        if 'phone_no' in data:
            print(serializer.validated_data)
            user = authenticate(phone_no=serializer.validated_data['phone_no'], password=serializer.validated_data['password'])
        if user:
          
            refresh = RefreshToken.for_user(user)
   
            try:
                access_token = str(refresh.access_token)
                
            except TokenError:
            
                return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'verified successfully.', 'access_token': access_token, 'user' : UserSignupSerializer(user).data,  'refresh_token':str(refresh)}, status=status.HTTP_200_OK)
            
            # Set the refresh token as a cookie in the response
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
                value=str(refresh),
                httponly=True,
                samesite=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'],
                secure=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'],
            )
         
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'], serializer_class=UserSignupSerializer)
    def google_login(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data['email']).first()
        if user:
            return Response(data=UserSignupSerializer(user).data, status=status.HTTP_200_OK)
        else:
            user_serilizer = UserSignupSerializer(data=data)
            user_serilizer.is_valid(raise_exception=True)
            user=user_serilizer.save()
            return Response(data=user_serilizer.data, status=status.HTTP_201_CREATED)