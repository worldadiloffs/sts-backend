from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from settings.models import CashBackSetting, Dokon, Shaharlar, Tumanlar , PaymentMethod, TolovUsullar , OrderSetting
from product.models import Product
from .models import Order, OrderItem , FirmaBuyurtma
from .serializers import OrderGetSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.http import JsonResponse

from drf_spectacular.utils import extend_schema

from rest_framework.throttling import ScopedRateThrottle

from account.models import User



def _validate_product_count(product_id, count):
    product = Product.objects.filter(id=product_id).first()
    if product and product.counts >= count:
        return True
    return False



def _order_item_to_dict(order_item) -> list[int]:
    error_product = []
    if order_item is None:
        return {"errors": True, "data": None}
    for i in order_item:
        validate_count = _validate_product_count(product_id=i['product_id'],count=i['quantity'])
        if not(validate_count):
            error_product.append({"product_id":i['product_id'], "quantity": i['quantity']})

    if len(error_product) > 0:
        return {"errors": True, "data": error_product}
    else:
        return {"errors": False, "data": order_item}




def __payment_method_to_dict(tolov_usullar, payment_method) -> int:
    payment = PaymentMethod.objects.filter(id=payment_method).first()
    if payment is not None:
        tolov_usul = TolovUsullar.objects.filter(id=tolov_usullar).first()
        for tolov in tolov_usul.payment_methods.all():
            if tolov.id == payment.pk:
                return {"errors": False, "payment_method_id": payment.pk}
        return {"errors": True, "data":{"payment_method_id": None}}
    return {"errors": True,  "data":{"payment_method_id": None}}


def _tolov_usullar_to_dict(tolov_usullar) ->dict:
    tolov = TolovUsullar.objects.filter(id=tolov_usullar).first()
    if tolov is not None:
        return {"errors": False, "tolov_usullar_id": tolov.pk}
    else:
        return {"errors": True, "data":{"tolov_usullar_id": None}}




def _punkit_to_dict(punkit) -> int:
    dokonlar = Dokon.objects.filter(id=punkit).first()
    if dokonlar is not None:
        return {"errors": False, "dokon_id": dokonlar.pk}
    else:
        return {"errors": True, "data":{"dokon_id": None}}



# cashback funtion user cashback validate 
def _validate_cashback(cash_price, user) -> float:
    ''' return true if cashback is valid else false  '''
    pass


def _validate_depozit(depozit, user) -> float:
    pass


def _redirect_payment(request, order_id):
    pass 





def _profile_update(first_name, last_name):
    pass 


def _firma_create_views(firma_nomi, zakas_id, user_id):
    user = User.objects.get(id=user_id)
    firma_nomi = FirmaBuyurtma.objects.create(firma_name=firma_nomi, buyurtma_raqami=zakas_id, user=user)
    firma_nomi.save()
    return firma_nomi.pk



class OrderCreateAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [JWTAuthentication ,]
    # throttle_scope = "authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]
    @extend_schema(
            request=OrderGetSerializer(),
            responses=OrderGetSerializer()
    )
    def post(self, request):
        # order items is  required fields 
        
        order_item_data = []
        
        first_name = request.data.get('firt_name', None)
        
        last_name = request.data.get("last_name", None)
        
        firma_nomi = request.data.get("firma_nomi", None) 
            
        profile_user = _profile_update(first_name=first_name, last_name=last_name)
        
        doller = OrderSetting.objects.first()
        doller_value =int(doller.doller * doller.nds / 10)
        zakas_id = (Order.objects.count() + 1000)
        request.data["zakas_id"] = zakas_id 
        if firma_nomi is not None:
            firma_id  = _firma_create_views(firma_nomi, zakas_id=zakas_id, user_id=request.user.id)
            request.data["firma_buyurtma"] = firma_id
        if request.data.get("order_items") is not None:
            order_validate = _order_item_to_dict(request.data.get("order_items"))
            if order_validate['errors']:
                return Response(data=order_validate, status=400)
            for item in request.data.get("order_items"):
                prod = Product.objects.get(id=item['product_id'])
                item_data = { "product": item['product_id'], "quantity": item['quantity'], "user": request.user.id, "zakas_id": zakas_id,"site_sts": True, "mahsul0t_narxi":int(prod.price * doller_value)}
                item_serializer = OrderItemSerializer(data=item_data)
                if item_serializer.is_valid(raise_exception=True):
                    item_serializer.save()
                    item_data['id'] = item_serializer.data.get('id')
                    order_item_data.append(item_data)
        else:
            return Response({"errors": "Invalid order items"}, status=200)
        #payment method is option fields 
        # if request.data.get("payment_method")  is not None:
        #     payment_validate = __payment_method_to_dict(request.data.get("payment_method"))
        #     if not(payment_validate['errors']):
        #         request.data["payment_method"] = payment_validate['payment_method_id']
        #     return Response(payment_validate, status=400)
        
        if request.data.get("tolov_usullar") is None:
            return Response({"errors": "Invalid tolov usullar"}, status=400)
        # tolov usullarni requeired fields
        tolov_usullar_validate = _tolov_usullar_to_dict(
            request.data.get("tolov_usullar")
        )
        if tolov_usullar_validate['errors']:
            return Response(tolov_usullar_validate, status=400)
        else:
            request.data["tolov_usullar"] = tolov_usullar_validate["tolov_usullar_id"]

        # punkit option fields
        if request.data.get("punkit") is not None:
            punkit_validate = _punkit_to_dict(request.data.get("punkit"))
            if punkit_validate['errors']:
                return Response(punkit_validate, status=400)
            else:
                request.data["punkit"] = punkit_validate["dokon_id"]

        # request.data["order_items"] =order_item_data
        request.data["site_sts"] = True
        request.data["user"] = request.user.id

        # cashback field option fields 
        if request.data.get("cashback") is not None:
            cashback_validate = _validate_cashback(
                request.data.get("cashback"), request.user
            )
            if bool(cashback_validate):
                request.data["cashback"] = cashback_validate
            else:
                return Response({"errors": "Invalid cashback amount"}, status=400)
            
        # depozit field option fields
        if request.data.get("depozit") is not None:
            depozit_validate = _validate_depozit(
                request.data.get("depozit"), request.user
            )
            if depozit_validate:
                request.data["depozit"] = depozit_validate
            else:
                return Response({"errors": "Invalid depozit amount"}, status=400)
        request.data["total_price"] = sum(
            [
                int(item["mahsul0t_narxi"]) * int(item["quantity"])
                for item in order_item_data
            ]
        )
        if request.data.get('shahar') is not None:
            shhar = Shaharlar.objects.get(name=request.data['shahar'])
            request.data['shahar'] = shhar.pk
        if request.data['tuman'] is not None:
            tuman = Tumanlar.objects.get(name=request.data['tuman'])
            request.data['tuman']=  tuman.pk
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            order_id = Order.objects.get(id=serializer.data.get('id'))
            for i in order_item_data:
                order_id.order_items.add(OrderItem.objects.get(id=i['id']))
            # payment_redirect = _redirect_payment(request=request, order_id=serializer.data.get('id'))
            order_serial = OrderGetSerializer(order_id)
            return Response(order_serial.data, status=201)
        return Response(serializer.errors, status=400)


class OrderGetAPIView(APIView):
    def get(self, request):
        order = Order.objects.all()
     
        serializer = OrderGetSerializer(order, many=True)
        return Response({"data": serializer.data, "errors": False, "message": ""})
       

class OrderUpdateAPIView(APIView):
    def patch(self, request, pk):
        pass # your code here


class OrderPaymentAPIView(APIView):
    def post(self, request, pk):
        pass # your code here
    


class VazvratProductAPIView(APIView):
    def post(self, request):
        pass # your code here


{
    "products": [
      { 
           "id": 1,
        "count": 2},
          { 
           "id": 1,
        "count": 2}
    ]
}


class STSCashbackMobile(APIView):
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



class UserOrderGet(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user 
        # if user.is_authenticated:
        order = Order.objects.all().order_by("created_at")
        serialzier = OrderGetSerializer(order, many=True)
        return JsonResponse({"data": serialzier.data, "errors": False, "message": "ok"}, safe=False) 
        # return JsonResponse({"data": None, "errors": True, "message": ""}, safe=False)
        