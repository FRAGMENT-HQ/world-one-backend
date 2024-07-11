from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import random
import requests
from communication.utils import send_otp


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], serializer_class=UserSignupSerializer)
    def signup(self, request):
        phone_no = request.data['phone_no']
        user = User.objects.filter(phone_no=phone_no).first()
        if user:
            return Response({'message': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        self.serializer_class = UserSignupSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        # genrate 6 digit otp
        otp = random.randint(100000, 999999)
        user.otp = otp
        user.save()
        print(user.otp)

        # try:
        #     access_token = str(refresh.access_token)

        # except TokenError:

        #     return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # response = Response({'detail': 'Created Sucesfull', 'access_token': access_token, 'user': UserSignupSerializer(
        #     user).data,  'refresh_token': str(refresh)}, status=status.HTTP_201_CREATED)

        # Set the refresh token as a cookie in the response
        # response.set_cookie(
        #     key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
        #     value=str(refresh),
        #     httponly=True,
        #     samesite=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'],
        #     secure=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'],
        # )
        print(otp)
        send_otp(str(otp), user.first_name, f'{user.country_code}{user.phone_no}', str(user.phone_no))
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=UserLoginSerializer)
    def verify_otp(self, request):
        data = request.data
        user = User.objects.filter(phone_no=data['phone_no']).first()

        print(user.otp,data)
        if user.otp == data['otp']:
            user.otp = ""
            user.save()

            refresh = RefreshToken.for_user(user)

            try:
                access_token = str(refresh.access_token)

            except TokenError:

                return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'verified successfully.', 'access_token': access_token, 'user': UserSignupSerializer(
                user).data,  'refresh_token': str(refresh)}, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['post'], serializer_class=UserLoginSerializer)
    def login(self, request):

        data = request.data
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)

        except Exception as e:
            return Response({'error': 'Invalid credentials', "data": serializer.errors}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        user = None
        if 'phone_no' in data:
            temp = User.objects.filter(phone_no=data['phone_no']).first()

            user = authenticate(
                phone_no=serializer.validated_data['phone_no'], password=serializer.validated_data['password'])
            
        if user and user.verification_status:

            refresh = RefreshToken.for_user(user)

            try:
                access_token = str(refresh.access_token)

            except TokenError:

                return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'verified successfully.', 'access_token': access_token, 'user': UserSignupSerializer(
                user).data,  'refresh_token': str(refresh)}, status=status.HTTP_200_OK)

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
        token = data['token']
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.verification_status:

            refresh = RefreshToken.for_user(user)

            try:
                access_token = str(refresh.access_token)

            except TokenError:

                return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'verified successfully.', 'access_token': access_token, 'user': UserSignupSerializer(
                user).data, }, status=status.HTTP_200_OK)

            # Set the refresh token as a cookie in the response
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'],
                value=str(refresh),
                httponly=True,
                samesite=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'],
                secure=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'],
            )

            return response
        
        elif user and not user.verification_status:
            return Response(status=status.HTTP_201_CREATED)

        else:

            # remove token from data
            data.pop('token')

            user_serilizer = UserSignupSerializer(data=data)
            user_serilizer.is_valid(raise_exception=True)
            user = user_serilizer.save()
            return Response(data=user_serilizer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], serializer_class=UserSignupSerializer)
    def completeProfile(self, request):
        data = request.data

        user = User.objects.filter(email=data['email']).first()
        if user:
            user.phone_no = data['phone_no']
            user.country_code = data['country_code']
            user.verification_status = True
            user.save()
            refresh = RefreshToken.for_user(user)

            try:
                access_token = str(refresh.access_token)

            except TokenError:

                return Response({'detail': 'Failed to generate access token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = Response({'detail': 'verified successfully.', 'access_token': access_token, 'user': UserSignupSerializer(
                user).data, }, status=status.HTTP_200_OK)

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
    def forgot_password(self, request):
        data = request.data
        user = User.objects.filter(email=data['email']).first()
        if user:
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    @action(detail=False, methods=['post'], serializer_class=UserSignupSerializer)
    def reset_password(self, request):
        data = request.data
        user = User.objects.filter(email=data['email']).first()
        if user:
            user.set_password(data['password'])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)