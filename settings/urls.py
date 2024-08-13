from django.urls import path
from .views import  SiteSettingsApiviews

app_name = 'settings'

urlpatterns = [
    path('sts/settings/', SiteSettingsApiviews.as_view()),
    
]

