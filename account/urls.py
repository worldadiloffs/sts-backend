from django.urls import path
from .views import (
    UserUPdate, UserUpdateAddress,  UserProfile, 
    Login, Register, VerifyOtp,
    ChangeTwoStepPassword, CreateTwoStepPassword,LogoutView , UserAdressCreate
)

from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

app_name = "account"

urlpatterns = [
    path('<str:site>/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:site>/account/logaut/',LogoutView.as_view(), name='auth_logout' ),
    path("<str:site>/account/profile/", UserProfile.as_view(), name="profile"),
    path("<str:site>/account/login/", Login.as_view(), name="login"),
    path("<str:site>/account/register/", Register.as_view(), name="register"),
    path("<str:site>/account/verify/", VerifyOtp.as_view(), name="verify-otp"),
    path("<str:site>/account/change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
    path("<str:site>/account/create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    path("<str:site>/account/users/<int:pk>/",csrf_exempt(UserUPdate.as_view()), name="users-detail"  ),
    path("<str:site>/account/address/", csrf_exempt(UserAdressCreate.as_view()), name="address-create" ),
    path("<str:site>/account/address/<int:pk>/", csrf_exempt(UserUpdateAddress.as_view()), name="address-update"),
]

