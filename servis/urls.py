from django.urls import path
from .views import HomePageViewsOne , ContactformApiView , VerifyphoneApiView

app_name ='servis'

urlpatterns = [
    path('servis-home/', HomePageViewsOne.as_view(), name='servis_home'),
    path('servis-contactform/', ContactformApiView.as_view(), name='contactform'),
    path('servis-verify-phone/', VerifyphoneApiView.as_view(), name='verify_phone'),
]
