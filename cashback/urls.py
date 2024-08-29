from django.urls import path
from .views import CashbackApiviews


urlpatterns = [
    path('sts/cashback/card/', CashbackApiviews.as_view(), name='cashback-card-sts'),
]
