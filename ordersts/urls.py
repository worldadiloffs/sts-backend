from django.urls import path

from ordersts.order_get_validate import OrderValudeView

app_name = 'ordersts'


from .views import OrderCreateAPIView
from .orderlocation import LocationAPIView
# from . import views


urlpatterns = [
    path('sts/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
    path('sts/orders/validate/', OrderValudeView.as_view(), name='order_get_validate'),
    path('sts/location/<int:pk>/', LocationAPIView.as_view(), name='location'),
    # path('sts/order/get/', views.OrderGetAPIView.as_view(), name='order_get'),
    # path('sts/order/post/', views.OrderPostAPIView.as_view(), name='order_post'),
    # path('sts/order/update/', views.OrderUpdateAPIView.as_view(), name='order_update'),
]

