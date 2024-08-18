from django.urls import path

from .views import (
    UsersList, UsersDetailUpdateDelete, UserProfile, 
    Login, Register, VerifyOtp,
    ChangeTwoStepPassword, CreateTwoStepPassword,LogoutView
)


app_name = "account"

urlpatterns = [
    # path("sts/account/list/", UsersList.as_view(), name="users-list"),
    path('sts/account/logaut/',LogoutView.as_view(), name='auth_logout' ),
    path("sts/account/profile/", UserProfile.as_view(), name="profile"),
    path("sts/account/login/", Login.as_view(), name="login"),
    path("sts/account/register/", Register.as_view(), name="register"),
    path("sts/account/verify/", VerifyOtp.as_view(), name="verify-otp"),
    path("sts/account/change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
    path("sts/account/create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    # path("sts/account/users/<int:pk>/", UsersDetailUpdateDelete.as_view(), name="users-detail"),
]