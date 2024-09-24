from django.urls import path
from .views import HomePageViewsOne

app_name ='servis'

urlpatterns = [
    path('servis-home/', HomePageViewsOne.as_view(), name='servis_home'),
]
