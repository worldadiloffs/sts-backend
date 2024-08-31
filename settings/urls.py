from django.urls import path
from .views import  PageApiviews, SiteSettingsApiviews  
from .rtsviews import RTSPageApiviews , RTSSiteSettingsApiviews

app_name = 'settings'

urlpatterns = [
    path('<str:site>/settings/', SiteSettingsApiviews.as_view()),
    path('<str:site>/page/', PageApiviews.as_view()),
    
]

