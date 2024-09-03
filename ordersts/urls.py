from django.urls import path
from .order_get_validate import OrderValudeView , MuddatliTOlovOrderView , DastafkaOrderView
from .views import OrderCreateAPIView , STSCashbackMobile , VazvratProductView

from ordersts.ordermobile.views import CashbackMobile ,  UserMobileToken 

from .order_get_user import OrderGetApiviews

app_name = 'ordersts'

urlpatterns = [
    path('<str:site>/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
    path('<str:site>/orders/validate/', OrderValudeView.as_view(), name='order_get_validate'),
    path('<str:site>/orders/muddatli_tolov/', MuddatliTOlovOrderView.as_view(), name='muddatli_tolov'),
    path('<str:site>/orders/dastafka/', DastafkaOrderView.as_view(),),
    path('<str:site>/cashback/validate/',  STSCashbackMobile.as_view(), name='cashback-validate'),
    path("<str:site>/orders/user-order-get/", OrderGetApiviews.as_view(), name="user-order-get"),
    path('<str:site>/vazvrat/orders/',  VazvratProductView.as_view(), name="vazvrat-product"),
    # mobile orders
    path('mobile/orders/cashback/', CashbackMobile.as_view(), name='mobile'),
    path('mobile/orders/token/', UserMobileToken.as_view(), name='token'),
]

# mobile order urls