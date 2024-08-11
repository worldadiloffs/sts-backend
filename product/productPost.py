from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from django.http import JsonResponse
from category.models import SuperCategory , MainCategory , SubCategory
from settings.models import CountSettings

class ProductPost(APIView):
    def post(self, request):
        """ product post funtion """
        try:
            articul = request.data['articul']
            price = request.data.get('price')
            material_nomer = request.get('material_nomer')
            product_name = request.data.get('product_name')
            count = request.data.get('count')
            super_id = request.data.get('super_id')
            main_id = request.data.get('main_id')
            sub_id = request.data.get('sub_id')
            site_sts = request.data.get('site_sts')
            site_rts = request.data.get('site_rts')
            product = Product.objects.filter(articul=articul).first()
            if product is not None:
                product.price=  price
                product.material_nomer = material_nomer
                product.product_name = product_name
                counts_settings =CountSettings.objects.filter(mainCategory__id=product.main_category.pk).exists()
                if counts_settings:
                    counts_max = CountSettings.objects.get(mainCategory__id=product.main_category.pk)
                    if count > counts_max.count:
                        count = counts_max.count
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
                product.save()
            else:
                product = Product()
                product.price = price
                product.product_name = product_name
                product.counts = count
                product.material_nomer = material_nomer
                product.site_rts = site_sts
                product.site_rts = site_rts
                if super_id is not None:
                    super_obj = SuperCategory.objects.get(id=super_id)
                    product.super_category = super_obj
                if main_id is not None:
                    main_obj = MainCategory.objects.get(id=main_id)
                    product.main_category=  main_obj
                if sub_id is not None:
                    sub_obj = SubCategory.objects.get(id=sub_id)
                    product.sub_category= sub_obj
                product.save()

            return JsonResponse({"data": "success", "errors": False, "message": ""}, safe=False)
        except Exception as e:
            return JsonResponse({"data": None, "errors": True, "message": f"{e}"})

class ProductUpdateAPiview(APIView):
    def post(self, request):
        try:
            count = request.data.get('count')
            articul = request.data['articul']
            if count is not None:
                product = Product.objects.get(articul = articul)
                counts_settings =CountSettings.objects.filter(mainCategory__id=product.main_category.pk).exists()
                if counts_settings:
                    counts_max = CountSettings.objects.get(mainCategory__id=product.main_category.pk)
                    if count > counts_max.count:
                        count = counts_max.count
                product.counts = count
                return JsonResponse({"data": "success", "errors": False, "message": ""}, safe=False)
        except Exception as e:
            return JsonResponse({"data": None, "errors": True, "message": f"{e}"}, safe=False)
            
            


class ProductPostApiView(APIView):
    def post(self, request):
        id = request.data.get('id')
        prod = Product.objects.get(id=id)
        prod.product_name = f"{prod.product_name} kamera"
        prod.save()
        return JsonResponse({"data": None}, safe=False)