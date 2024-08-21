from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.http import JsonResponse




def _order_item_to_dict(order_item) -> list[int]:
    pass


def __payment_method_to_dict(tolov_usullar, payment_method) -> int:
    pass


def _tolov_usullar_to_dict(tolov_usullar) -> int:
    pass


def _punkit_to_dict(punkit) -> int:
    pass

# cashback funtion user cashback validate 
def _validate_cashback(cash_price, user) -> float:
    ''' return true if cashback is valid else false  '''
    pass


def _validate_depozit(depozit, user) -> float:
    pass


def _redirect_payment(request, order_id):
    pass 


class OrderCreateAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [JWTAuthentication , ]

    def post(self, request):
        # order items is  required fields 
        if request.data.get("order_items") is not None:
            order_validate = _order_item_to_dict(request.data.get("order_items"))
            if order_validate is None:
                return Response({"errors": "Invalid product"}, status=400)
            for item in request.data.get("order_items"):
                item_serializer = OrderItemSerializer(data=item)
                if item_serializer.is_valid():
                    item_serializer.save(user=request.user)
                return Response(item_serializer.error_messages, status=400)
            
        #payment method is option fields 
        if request.data["payment"]  is not None:
            payment_validate = __payment_method_to_dict(request.data.get("payment"))
            if bool(payment_validate):
                request.data["payment"] = payment_validate
            request.data["payment"] = payment_validate

        # address option fields 
        if request.data["addres"] is not None:
            addres_validate = __payment_method_to_dict(request.data.get("addres"))
            if bool(addres_validate):
                request.data["addres"] = addres_validate

        if request.data.get("tolov_usullar") is None:
            return Response({"errors": "Invalid tolov usullar"}, status=400)
        # tolov usullarni requeired fields
        tolov_usullar_validate = _tolov_usullar_to_dict(
            request.data.get("tolov_usullar")
        )
        # punkit option fields
        if request.data["punkit"] is not None:
            punkit_validate = _punkit_to_dict(request.data.get("punkit"))
            request.data["punkit"] = punkit_validate

        request.data["order_items"] = order_validate
        request.data["tolov_usullar"] = tolov_usullar_validate
        request.data["site_sts"] = True
        request.data["user"] = request.user

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
                item["price"] * item["quantity"]
                for item in request.data.get("order_items")
            ]
        )
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            payment_redirect = _
            return Response(serializer.data, status=201)
        


class OrderUpdateAPIView(APIView):
    def patch(self, request, pk):
        pass # your code here


class OrderPaymentAPIView(APIView):
    def post(self, request, pk):
        pass # your code here
    


class VazvratProductAPIView(APIView):
    def post(self, request):
        pass # your code here
