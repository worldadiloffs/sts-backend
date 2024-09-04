from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order 
from  .serializers import  OrderGetUserSerializer


class OrderGetApiviews(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, site):
        user = request.user
        if user.is_authenticated:
            if site =='sts':
                order = Order.objects.filter(user__id=user.id, order_close=True,  site_sts=True).order_by("-created_at")
                hozirgi_zakaslar = Order.objects.filter(user__id=user.id, order_close=False,  site_sts=True).order_by("-created_at")
            if site == 'rts':
                order = Order.objects.filter(user__id=user.id, order_close=True,  site_rts=True).order_by("-created_at")
                hozirgi_zakaslar = Order.objects.filter(user__id=user.id, order_close=False,  site_rts=True).order_by("-created_at")
            serializer = OrderGetUserSerializer(order, many=True)
            zakas_lar = []
            if serializer.data:
                for i in serializer.data:
                    zakas_lar.append({
                        "order_items": i['order_items'],
                        "status_color": i['status_color'],
                        "order": i['order_obj'], })
            
            hozir_serializer = OrderGetUserSerializer(hozirgi_zakaslar, many=True)
            hozir = []
            if hozir_serializer:
                for i in hozir_serializer.data:
                    hozir.append({
                        "mobile": {
                            "zakas_id": i['zakas_id'],
                            "sana": f"{i['created_at'].strftime("%B %d %Y %H:%M")}",
                            "status": i['status'],
                            "umumiy_summa": i['total_summa'],
                            "tushgan_cash_summa": i['tushadigan_cash_summa']
                            
                        },
                        "order_items": i['order_items'],
                        "status_color": i['status_color'],
                        "order": i['order_obj'], })
            return Response({"data": {"hozir": hozir, "barchasi": zakas_lar }, "errors": False, "message": ""}, status=status.HTTP_200_OK)
        return JsonResponse({'data': None, 'errors': True, 'message': ''}, safe=False)
    