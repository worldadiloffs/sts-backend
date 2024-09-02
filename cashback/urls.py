from django.urls import path
from .views import CashbackApiviews  , CashbackMobileApiviews

app_name = 'cashback'


urlpatterns = [
    path('<str:site>/cashback/card/', CashbackApiviews.as_view(), name='cashback-card-sts'),
    path('mobile/cashback/cards/', CashbackMobileApiviews.as_view(), name='cashback-card-mobile')
]

