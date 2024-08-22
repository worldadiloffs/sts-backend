from django.urls import path
from .views import  SiteSettingsApiviews , ShaharLarPostApiviews

app_name = 'settings'

urlpatterns = [
    path('sts/settings/', SiteSettingsApiviews.as_view()),
    path('shaharlar/post/', ShaharLarPostApiviews.as_view()),
    
]

