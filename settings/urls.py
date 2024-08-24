from django.urls import path
from .views import  PageApiviews, SiteSettingsApiviews  
from .rtsviews import RTSPageApiviews , RTSSiteSettingsApiviews

app_name = 'settings'

urlpatterns = [
    path('sts/settings/', SiteSettingsApiviews.as_view()),
    path('sts/page/', PageApiviews.as_view()),
    # rts site uchun settings ve pageleri getirmek
    path('rts/settings/', RTSSiteSettingsApiviews.as_view()),
    path('rts/page/', RTSPageApiviews.as_view()),
    
]

