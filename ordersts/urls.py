from django.urls import path
from .order_get_validate import OrderValudeView , MuddatliTOlovOrderView , DastafkaOrderView
from .views import OrderCreateAPIView , STSCashbackMobile , VazvratProductView , ContactFormApiveiws

from ordersts.ordermobile.views import CashbackMobile ,  UserMobileToken 
from .cupon import CoponPostApiviews

from .order_get_user import OrderGetApiviews
from ordersts.payme.views import TestViewPayme , checkout_view
from ordersts.clicks.click import TestView
from ordersts.clicks.create_payment import create_click_payment

app_name = 'ordersts'

urlpatterns = [
    path('<str:site>/orders/craate/', OrderCreateAPIView.as_view(), name='order_create'),
    path('<str:site>/orders/validate/', OrderValudeView.as_view(), name='order_get_validate'),
    path('<str:site>/orders/muddatli_tolov/', MuddatliTOlovOrderView.as_view(), name='muddatli_tolov'),
    path('<str:site>/orders/dastafka/', DastafkaOrderView.as_view(),),
    path('<str:site>/cashback/validate/',  STSCashbackMobile.as_view(), name='cashback-validate'),
    path("<str:site>/orders/user-order-get/", OrderGetApiviews.as_view(), name="user-order-get"),
    path('<str:site>/vazvrat/orders/',  VazvratProductView.as_view(), name="vazvrat-product"),
    path('<str:site>/cupon/validate/', CoponPostApiviews.as_view(), name='cupon-validate'),
    path('<str:site>/contact-form/', ContactFormApiveiws.as_view(), name='contact-form'),

    # mobile orders
    path('mobile/orders/cashback/', CashbackMobile.as_view(), name='mobile'),
    path('mobile/orders/token/', UserMobileToken.as_view(), name='token'),
    # payme url 
    path('check/paycom/', TestViewPayme.as_view()),
    path('check-order/', checkout_view , name='check-order'),

    # click url 
    path('click/transaction/', TestView.as_view(), name='click-transaction'),
    path('create-click-payment/', create_click_payment, name='create-click-payment'),
]

# mobile order urls