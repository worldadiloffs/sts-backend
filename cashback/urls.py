from django.urls import path
from .views import CashbackApiviews

app_name = 'cashback'


urlpatterns = [
    path('rts/cashback/card/', CashbackApiviews.as_view(), name='cashback-card-sts'),
]
