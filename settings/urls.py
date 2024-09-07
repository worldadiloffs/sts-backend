from django.urls import path
from .views import  PageApiviews, SiteSettingsApiviews  , PageContentApiviews


app_name = 'settings'

urlpatterns = [
    path('<str:site>/settings/', SiteSettingsApiviews.as_view(), name="site-settings"),
    path('<str:site>/page/', PageApiviews.as_view(), name="page-settings"),
    path('<str:site>/page-content/<str:slug>/', PageContentApiviews.as_view(), name="page-content-detail"),
    
]

