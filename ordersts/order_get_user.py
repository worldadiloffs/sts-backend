from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order , OrderItem 
from  .serializers import OrderGetSerializer, OrderGetUserSerializer, OrderSerializer, OrderItemSerializer


data = {
    "Buyurtma_raqami": "123456",
    "status": "bekor",
    "Buyurtma_vaqti": "2022-01-01 10:00:0",
    "Yetkazib_berish_vaqti": "2022-01",
    "Tolov_usuli": "Karta",
    "Qabul_qilish_usuli": "yetkazib berish",
    "Buyurtma_turi": "onliyn",
    "Yetkazib_berish_manzili": "Jizzi",
    "narxi": "43443434343 summa",
    "yetkazib_berish": 0,
    "Jami": 0,
}




class OrderGetApiviews(APIView):
    def get(self, request):
        user = request.user
        # if user.is_authenticated:
        order = Order.objects.all()
        serializer = OrderGetUserSerializer(order, many=True)
        zakas_lar = []
        if serializer.data:
            for i in serializer.data:
                zakas_lar.append({
                      "order_items": i['order_items'],
                      "order": i['order_obj'], })
                # zakas_lar.sort(key=lambda x: x['tavarlar']['created_at'], reverse=True)
            
        return Response({"data": zakas_lar, "errors": False, "message": ""}, status=status.HTTP_200_OK)