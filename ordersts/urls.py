from django.urls import path

app_name = 'ordersts'

from .views import OrderCreateAPIView
# from . import views


urlpatterns = [
    path('sts/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
]

