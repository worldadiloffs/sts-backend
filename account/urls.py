from django.urls import path

from .views import (
    UserUPdate, UserUpdateAddress, UsersList, UsersDetailUpdateDelete, UserProfile, 
    Login, Register, VerifyOtp,
    ChangeTwoStepPassword, CreateTwoStepPassword,LogoutView , UserAdressCreate
)

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .rtsviews import RTSUserProfile, RTSUserUPdate, RTSUserAdressCreate , RTSRegister, RTSUserUpdateAddress


app_name = "account"

urlpatterns = [
    path('sts/account/logaut/',LogoutView.as_view(), name='auth_logout' ),
    path("sts/account/profile/", UserProfile.as_view(), name="profile"),
    path("sts/account/login/", Login.as_view(), name="login"),
    path("sts/account/register/", Register.as_view(), name="register"),
    path("sts/account/verify/", VerifyOtp.as_view(), name="verify-otp"),
    path("sts/account/change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
    path("sts/account/create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    path("sts/account/users/<int:pk>/",csrf_exempt(UserUPdate.as_view()), name="users-detail"  ),
    path("sts/account/address/", csrf_exempt(UserAdressCreate.as_view()), name="address-create" ),
    path("sts/account/address/<int:pk>/", csrf_exempt(UserUpdateAddress.as_view()), name="address-update"),
    # rts site uchun api 
    path("rts/account/profile/", RTSUserProfile.as_view(), name="rts-profile"),
    path("rts/account/register/", RTSRegister.as_view(), name="rts-register"),
    path("rts/account/verify/", VerifyOtp.as_view(), name="rts-verify-otp"),
    path("rts/account/users/<int:pk>/",csrf_exempt(RTSUserUPdate.as_view()), name="rts-users-detail"  ),
    path("rts/account/address/", csrf_exempt(RTSUserAdressCreate.as_view()), name="rts-address-create" ),
    path("rts/account/address/<int:pk>/", csrf_exempt(RTSUserUpdateAddress.as_view()), name="rts-address-update"),
]