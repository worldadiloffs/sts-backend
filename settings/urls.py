from django.urls import path
from .views import  PageApiviews, SiteSettingsApiviews  , PageContentApiviews , ServisPageApiviews , ShaharLarPostApiviews


app_name = 'settings'

urlpatterns = [
    path('<str:site>/settings/', SiteSettingsApiviews.as_view(), name="site-settings"),
    path('<str:site>/page/', PageApiviews.as_view(), name="page-settings"),
    path('<str:site>/page-content/<str:slug>/', PageContentApiviews.as_view(), name="page-content-detail"),
    path('<str:site>/servis-page/', ServisPageApiviews.as_view(), name='servis-page-content-list'),
    path('shahar-lar/', ShaharLarPostApiviews.as_view(), name='shahar-lar-post')  # this is for create shahar and tuman in bulk by post request  # example data = [{"title": "Shahar 1", "title_ru": "��ахар 1", "shahar": [{"name": "Tuman 1", "name_ru": "Тум
    
]

