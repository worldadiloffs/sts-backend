from django.urls import path

from ordersts.order_get_validate import OrderValudeView , MuddatliTOlovOrderView , DastafkaOrderView
from .views import OrderCreateAPIView , STSCashbackMobile 
from .rtsviews import RTSOrderCreateAPIView , RTSOrderGetAPIView , RTSOrderValudeView , RTSMuddatliTOlovOrderView
from ordersts.ordermobile.views import CashbackMobile ,  UserMobileToken

from .order_get_user import OrderGetApiviews , RTSOrderGetApiviews

app_name = 'ordersts'

urlpatterns = [
    path('sts/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
    path('sts/orders/validate/', OrderValudeView.as_view(), name='order_get_validate'),
    path('sts/orders/get/', RTSOrderGetAPIView.as_view(), name='order_get'),
    path('sts/orders/muddatli_tolov/', MuddatliTOlovOrderView.as_view(), name='muddatli_tolov'),
    path('sts/orders/dastafka/', DastafkaOrderView.as_view(),),
    path('sts/cashback/validate/',  STSCashbackMobile.as_view(), name='cashback-validate'),
    path("sts/orders/user-order-get/", OrderGetApiviews.as_view(), name="user-order-get"),
    # rts orders
    path('rts/orders/craate/', RTSOrderCreateAPIView.as_view(), name='order_create'),
    path('rts/orders/validate/', RTSOrderValudeView.as_view(), name='order_get_validate'),
    path('rts/orders/muddatli_tolov/', RTSMuddatliTOlovOrderView.as_view(), name='order_muddatli_tolov'),
    path('rts/cashback/validate/',  STSCashbackMobile.as_view(), name='cashback-validate'),
    path('rts/orders/dastafka/', DastafkaOrderView.as_view(),),
    path("rts/orders/user-order-get/", RTSOrderGetApiviews.as_view(), name="user-order-get"),
    # mobile orders
    path('mobile/orders/cashback/', CashbackMobile.as_view(), name='mobile'),
    path('mobile/orders/token/', UserMobileToken.as_view(), name='token'),
]



