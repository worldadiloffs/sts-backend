import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from extensions.code_generator import get_client_ip
import threading
from product.models import Product

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]  # Birinchi IP manzil asl foydalanuvchi IPsi bo'ladi
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

def my_function(data):
    print(f"Bu xabar {data} !")
    product = Product.objects.get(id=data)
    print(f"Bu xabar {product.product_name}!")
    # print(f"Bu xabar {timess} shundan keyin chiqadi!")
    print("Bu xabar 5 soniyadan keyin chiqadi!")

class LocationAPIView(APIView):
    def get(self, request, pk=None):
    # 5 soniyadan keyin funksiyani ishga tushirish uchun Timer yaratish
        timer = threading.Timer(5.0, my_function, args={pk})

        # Timer'ni boshlash
        timer.start()
        return Response({"message": "Location API ishlaydi"}, status=200)

print("Bu xabar darhol chiqadi!")
       




