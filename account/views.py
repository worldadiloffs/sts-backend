import random
import requests
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import User, UserAddress
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User 
from drf_spectacular.utils import extend_schema

from cashback.models import CashbackKard

from .serializers import (
    UserAdressSerializer,
    UserProfileSerializer,
    AuthenticationSerializer,
    OtpSerializer,
    ChangeTwoStepPasswordSerializer,
    CreateTwoStepPasswordSerializer,
)
from .send_otp import send_otp

from config.settings import CRM_KEY , CRM_TOKEN , CRM_URL

# from permissions import IsSuperUser
from extensions.code_generator import get_client_ip

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, site):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                status=status.HTTP_205_RESET_CONTENT, content_type="status seksesfull"
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, content_type="status error"
            )



class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, site):
        user = request.user
        if user.is_authenticated:
                serializer = UserProfileSerializer(user)
                addres_serialzier = None
                addres_bool= UserAddress.objects.filter(user=user).first()
                if addres_bool is not None:
                    addres_serialzier = UserAdressSerializer(addres_bool)
                
                return Response({"data": {"user": serializer.data, "address": addres_serialzier,  "is_login": True}}, status=status.HTTP_200_OK)
        else:
            return Response({"data": {"user": None, "is_login": False}}, status=status.HTTP_403_FORBIDDEN)
        




class UserUPdate(APIView):
    def put(self, request, site, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        




class UserAdressCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]
    @extend_schema(
            request=UserAdressSerializer(),
            responses=UserAdressSerializer()
    )
    
    
    def post(self, request, site):
        user = request.user
        request.data['user'] = user.id
        serializer = UserAdressSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class UserUpdateAddress(APIView):
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
            request=UserAdressSerializer(),
            responses= UserAdressSerializer()
    )
    def put(self, request,site , pk):
        address = get_object_or_404(UserAddress, pk=pk)
        user = request.user
        if user!= address.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserAdressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        


class Login(APIView):
    """
    post:
        Send mobile number for Login.
        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]

    def post(self, request, site):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")

            user_is_exists: bool = (
                User.objects.filter(phone=received_phone).values("phone").exists()
            )
            if not user_is_exists:
                return Response(
                    {
                        "No User exists.": "Please enter another phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
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


class Register(APIView):
    """
    post:
        Send mobile number for Register.
        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]

    def post(self, request, site):
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



def _cashback_create(phone, site):
    user = User.objects.get(phone=phone)
    if site == "sts":
        cashback :bool = CashbackKard.objects.filter(user=user, site_sts=True).exists()
        if not(cashback):
            cashacks = CashbackKard()
            cashacks.card = _cart_random()
            cashacks.site_sts = True
            cashacks.user = user
            cashacks.save()
            return True
        return False
    if site == "rts":
        cashback :bool = CashbackKard.objects.filter(user=user, site_rts=True).exists()
        if not(cashback):
            cashacks = CashbackKard()
            cashacks.card = _cart_random()
            cashacks.site_rts = True
            cashacks.user = user
            cashacks.save()
            return True
        return False




class VerifyOtp(APIView):
    """
    post:
        Send otp code to verify mobile number and complete authentication.
        parameters: [otp,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "verify_authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]

    def post(self, request, site):
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
                    
                    datase = User.objects.get(phone=phone)
                    if site == "sts":
                        datase.site_sts= True
                    if site == "rts":
                        datase.site_rts= True
                    datase.save()
                        # threading.Timer(3, _request_user_crm, phone).start()
                    _cashback_create(phone, site=site)


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


class CreateTwoStepPassword(APIView):
    """
    post:
        Send a password to create a two-step-password.

        parameters: [new_password, confirm_new_password]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, site):
        if request.user.two_step_password:
            return Response(
                {"Error!": "Your request could not be approved."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = CreateTwoStepPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get("new_password")
        try:
            _: None = validate_password(new_password)
        except ValidationError as err:
            return Response({"errors": err}, status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        user.set_password(new_password)
        user.two_step_password = True
        user.save(update_fields=["password", "two_step_password"])
        return Response(
            {"Successful.": "Your password was changed successfully."},
            status=status.HTTP_200_OK,
        )


class ChangeTwoStepPassword(APIView):
    """
    post:
        Send a password to change a two-step-password.

        parameters: [old_password, new_password, confirm_new_password,]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, site):
        if request.user.two_step_password:
            serializer = ChangeTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_password = serializer.data.get("new_password")

            try:
                _: None = validate_password(new_password)
            except ValidationError as err:
                return Response(
                    {"errors": err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            old_password = serializer.data.get("old_password")
            user = get_object_or_404(get_user_model(), pk=request.user.pk)
            check_password: bool = user.check_password(old_password)
            if check_password:
                user.set_password(new_password)
                user.save(update_fields=["password"])

                return Response(
                    {
                        "Successful.": "Your password was changed successfully.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Error!": "The password entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        return Response(
            {
                "Error!": "Your request could not be approved.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
