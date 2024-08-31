from django.urls import path
from .views import CashbackApiviews , RTSCashbackApiviews , CashbackMobileApiviews

app_name = 'cashback'


urlpatterns = [
    path('sts/cashback/card/', CashbackApiviews.as_view(), name='cashback-card-sts'),
    path('rts/cashback/card/', RTSCashbackApiviews.as_view(), name='cashback-card-rts'),
    path('mobile/cashback/card/', CashbackMobileApiviews.as_view(), name='cashback-card-mobile')
]
