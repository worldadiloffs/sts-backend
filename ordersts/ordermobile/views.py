from rest_framework.views import APIView
from account.models import User
from django.http import JsonResponse

from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Product
from settings.models import CashBackSetting, OrderSetting


class UserMobileToken(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        user = User.objects.filter(phone=phone).first()
        if user:
            token = RefreshToken.for_user(user)
            return Response({"refresh": str(token), "access": str(token.access_token)}, status=200)
        else:
            user = User.objects.create(phone=phone, crm_user=True)
            user.save()
            token = RefreshToken.for_user(user)
            return Response({"refresh": str(token), "access": str(token.access_token)}, status=200)



class CashbackMobile(APIView):
    def post(self, request):
        products = request.data['products']
        order_setting = OrderSetting.objects.first()
        doller_value = int(order_setting.doller * order_setting.nds / 10)
        berialadigan_cashback = 0
        if products is not None:
            for product in products:
                product_obj = Product.objects.get(id=product["id"])
                cashback_setting = CashBackSetting.objects.filter(product=product_obj).first()
                if cashback_setting:
                    berialadigan_cashback += cashback_setting.cashback_foiz * product["count"] * product_obj.price *doller_value
                
                else:
                    prod = Product.objects.get(id=product["id"])
                    sub_id = prod.sub_category.pk
                    cashback_setting = CashBackSetting.objects.filter(category_tavar__id=sub_id).first()
                    if cashback_setting:
                        berialadigan_cashback += int(cashback_setting.cashback_foiz * product["count"] * product_obj.price * doller_value * 0.01)
            return JsonResponse({"data": berialadigan_cashback, "errors": False, "message": "ok"},safe=False)
        return JsonResponse({"data": None, "errors": True, "message": "Productlar mavjud"}, safe=False)




{
    "cashback_summa": 100,
    "dokon_id": 1,
    "payment_method_id": 1,
    "products": [
        {"id": 1, "count": 2, "price": 1000000000000000},
        {"id": 2, "count": 3, "price": 2000000000000000}
    ],
    "hisobot": [
        { 
        "zakas_id": 1,
        "tolov_usullar": "site , mobile , dokon",
        "yechilgan_summa": 1000000000000000,
        "tushgan_summa": 1000000000000000,
        "date": "2022-01-01",
        "time": "10:00:00"
        }
    ],
        
    "depozit_summa": 1000,  
}