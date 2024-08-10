from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from django.http import JsonResponse
from category.models import SuperCategory , MainCategory , SubCategory


class ProductPost(APIView):
    def post(self, request):
        """ product post funtion """
        articul = request.data['articul']
        price = request.data.get('price')
        material_nomer = request.get('material_nomer')
        product_name = request.data.get('product_name')
        count = request.data.get('count')
        super_id = request.data.get('super_id')
        main_id = request.data.get('main_id')
        sub_id = request.data.get('main_id')
        product = Product.objects.filter(articul=articul).first()
        if product is not None:
            product.price=  price
            product.material_nomer = material_nomer
            product.product_name = product_name
            product.counts = count
        if super_id is not None:
            super_obj = SuperCategory.objects.get(id=super_id)
            product.super_category = super_obj
        if main_id is not None:
            main_obj = MainCategory.objects.get(id=main_id)
            product.main_category=  main_obj
        if sub_id is not None:
            sub_obj = SubCategory.objects.get(id=sub_id)
            product.sub_category= sub_obj
        

class ProductPostApiView(APIView):
    def post(self, request):
        id = request.data.get('id')
        prod = Product.objects.get(id=id)
        prod.product_name = f"{prod.product_name} kamera"
        prod.save()
        return JsonResponse({"data": None}, safe=False)