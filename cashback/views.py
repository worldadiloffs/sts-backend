from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

from product.models import Product
from settings.models import CashBackSetting, OrderSetting

from .models import CashbackKard
from .serialziers import CashbackKardSerializer, CashbackMobileSerialziers


# Create your views here.


def cashback_values(products):
    order_setting = OrderSetting.objects.first()
    doller_value = int(order_setting.doller * order_setting.nds / 10)
    berialadigan_cashback = 0
    if products is not None:
        for product in products:
            product_obj = Product.objects.get(id=product["id"])
            cashback_setting = CashBackSetting.objects.filter(product=product_obj).first()
            if cashback_setting is not None:
                berialadigan_cashback += cashback_setting.cashback_foiz * product["count"] * product_obj.price *doller_value *0.01
            else:
                prod = Product.objects.get(id=product["id"])
                sub_id = prod.sub_category.pk
                cashback_setting = CashBackSetting.objects.filter(category_tavar__id=sub_id).first()
                if cashback_setting is not None:
                    berialadigan_cashback += int(cashback_setting.cashback_foiz * product["count"] * product_obj.price * doller_value * 0.01)
        return {"data": berialadigan_cashback, "errors": False, "message": "ok"}
    return {"data": 0, "errors": True, "message": "Product cashback validate 0"}





class CashbackApiviews(APIView):
    def get(self, request, site):
        user = request.user
        if user.is_authenticated:
            if site == "sts":
                cashback = CashbackKard.objects.filter(user=user, site_sts=True).first()
            if site == "rts":
                cashback = CashbackKard.objects.filter(user=user, site_rts=True).first()
            if cashback is not None:
                serialzier = CashbackKardSerializer(cashback)
                return JsonResponse({"data": serialzier.data, "errors": False, "message": "ok"}, safe=False)
            return JsonResponse({"data": None, "errors": True, "message": "Kashback kard mavjud"}, safe=False)
        return JsonResponse({"data": None, "errors": True, "message": "Siz faol emasiz"}, safe=False)

class CashbackMobileApiviews(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            cashback = CashbackKard.objects.filter(user=user, site_sts=True).first()
            if cashback is not None:
                serialzier = CashbackMobileSerialziers(cashback)
                return JsonResponse({"data": serialzier.data, "errors": False, "message": "ok"}, safe=False)
            return JsonResponse({"data": None, "errors": True, "message": "Kashback kard mavjud"}, safe=False)
        return JsonResponse({"data": None, "errors": True, "message": "Siz faol emasiz"}, safe=False)
