import random
import threading
import requests
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache

from cashback.models import CashbackKard
from .models import User, UserAddress
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User 
from drf_spectacular.utils import extend_schema

from .serializers import (
    UserAdressSerializer,
    UsersListSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    AuthenticationSerializer,
    OtpSerializer,
    ChangeTwoStepPasswordSerializer,
    CreateTwoStepPasswordSerializer,
)
from .send_otp import send_otp

# from permissions import IsSuperUser
from extensions.code_generator import get_client_ip


class RTSUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_authenticated:
                serializer = UserProfileSerializer(user)
                addres_bool:bool  = UserAddress.objects.filter(user=user).exists()
                if addres_bool:
                    addres = UserAddress.objects.get(user=user)
    
                    addres_serialzier = UserAdressSerializer(addres) if addres else None
                    addres_data = addres_serialzier.data
                else:
                    addres_data = None
   
                # client_ip = "213.230.120.73"
                # Replace this with your actual API request
              
                    
                return Response({"data": {"user": serializer.data, "address": addres_data, "is_login": True}}, status=status.HTTP_200_OK)
        else:
            return Response({"data": {"user": None, "is_login": False}}, status=status.HTTP_403_FORBIDDEN)
        




class RTSUserUPdate(APIView):
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserDetailUpdateDeleteSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        



class RTSUserAdressCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
            request=UserAdressSerializer(),
            responses=UserAdressSerializer()
    )
    
    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        serializer = UserAdressSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RTSUserUpdateAddress(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
            request=UserAdressSerializer(),
            responses= UserAdressSerializer()
    )
    def put(self, request, pk):
        address = get_object_or_404(UserAddress, pk=pk)
        user = request.user
        if user!= address.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserAdressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class RTSRegister(APIView):
    """
    post:
        Send mobile number for Register.
        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    # throttle_scope = "authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")

            user_is_exists: bool = (
                get_user_model()
                .objects.filter(phone=received_phone)
                .values("phone")
                .exists()
            )
            if user_is_exists:
                return send_otp(
                    request,
                    phone=received_phone,
                )
            # The otp code is sent to the user's phone number for authentication
            return send_otp(
                request,
                phone=received_phone,
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )



def _cart_random():
    return int(f"8860{random.randint(100000000, 999999999)}")



def _cashback_create_rts(phone):
    user = User.objects.get(phone=phone)
    cashback :bool = CashbackKard.objects.filter(user=user, site_rts=True).exists()
    if not(cashback):
        cashacks = CashbackKard()
        cashacks.card = _cart_random()
        cashacks.user = user
        cashacks.site_rts = True
        cashacks.save()
        return True
    return False

class RTSVerifyOtp(APIView):
    """
    post:
        Send otp code to verify mobile number and complete authentication.
        parameters: [otp,]
    """

    # permission_classes = [
    #     AllowAny,
    # ]
    # throttle_scope = "verify_authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]

    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            two_step_passwords = serializer.data.get("two_step_passwords")
            received_code = serializer.data.get("code")
            ip = get_client_ip(request)
            phone = cache.get(f"{ip}-for-authentication")
            otp = cache.get(phone)
            if otp is not None:
                if otp == received_code:
                    user, created = get_user_model().objects.get_or_create(phone=phone)
                    if user.two_step_password:
                        cache.set(f"{ip}-for-two-step-password", user, 250)
                        check_password: bool = user.check_password(two_step_passwords)
                        if check_password:
                            refresh = RefreshToken.for_user(user)
                            cache.delete(phone)
                            cache.delete(f"{ip}-for-authentication")

                            context = {
                                "created": created,
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            }
                            return Response(context)
                        return Response(
                            {
                                "Thanks": "Please enter your two-step password",
                            },
                            status=status.HTTP_200_OK,
                        )

                    refresh = RefreshToken.for_user(user)
                    cache.delete(phone)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    # if created:
                    #     datase = Hamyon.objects.create(id=phone)
                    #     datase.save()

                    if created:
                        rts_user =User.objects.get(phone=phone)
                        rts_user.site_rts = True
                        rts_user.save()
                    _cashback_create_rts(phone=phone)

                    return Response(
                        context,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "Incorrect code.": "The code entered is incorrect.",
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {
                        "Code expired.": "The entered code has expired.",
                    },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

