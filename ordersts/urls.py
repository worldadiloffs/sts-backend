from django.urls import path

from ordersts.order_get_validate import OrderValudeView

app_name = 'ordersts'


from .views import OrderCreateAPIView
from .orderlocation import LocationAPIView
# from . import views


urlpatterns = [
    path('sts/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
    path('sts/orders/validate/', OrderValudeView.as_view(), name='order_get_validate'),
    path('location/', LocationAPIView.as_view(), name='order_list'),
]

