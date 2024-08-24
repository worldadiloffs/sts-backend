from django.urls import path

from ordersts.order_get_validate import OrderValudeView

app_name = 'ordersts'


from .views import OrderCreateAPIView
from .rtsviews import RTSOrderCreateAPIView , RTSOrderGetAPIView , RTSOrderValudeView


urlpatterns = [
    path('sts/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
    path('sts/orders/validate/', OrderValudeView.as_view(), name='order_get_validate'),
    path('sts/orders/get/', RTSOrderGetAPIView.as_view(), name='order_get'),
    # rts orders
    path('rts/orders/craate/', RTSOrderCreateAPIView.as_view(), name='order_create'),
    path('rts/orders/validate/', RTSOrderValudeView.as_view(), name='order_get_validate'),
]

