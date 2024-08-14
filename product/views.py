from rest_framework.views import APIView
from .serialzier import ImagePostSeriazilizer, ParemententCategorySerialzeir, ProductDetailSerialzeir, ProductListMiniSerilizers , ProductSerialzier , ImageSeriazilizer
from .models import Product , Image
from category.models import MainCategory, SubCategory, SuperCategory
from category.serializers import (
    MainCategortStsSerializer,
    SuperCategoryStsSerializer,
)
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from drf_spectacular.utils import extend_schema


from rest_framework.parsers import MultiPartParser , FormParser



class ProductListMiniView(APIView):
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
        responses=ProductListMiniSerilizers
    )
    def get(self, request):
        product = Product.objects.all()
        seriazleir = ProductListMiniSerilizers(product, many=True)
        return JsonResponse(
            {"data": seriazleir.data, "errors": False, "message": ""}, safe=False
        )
    



class ImageProductApiview(APIView):
    parser_classes =[MultiPartParser, FormParser]
    def post(self, request):
        serialzier = ImagePostSeriazilizer(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return JsonResponse({"data": serialzier.data, "errors":False, "message": ""},safe=False)
        return JsonResponse({"data": None, "errors":False, "message": ""}, safe=False)
    
    def get(self, request):
        image = Image.objects.all()
        seriazlier =ImagePostSeriazilizer(image, many=True)
        return JsonResponse(seriazlier.data)




class ProductDetailApiview(APIView):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug, status=True, site_sts=True)
        data = None
        if product.main_category is not None:
            main_category_product = Product.objects.filter(main_category__id=product.main_category.pk, status=True, site_sts=True)[:5]
            main_serialzier = ProductListMiniSerilizers(main_category_product, many=True)
            data = main_serialzier.data 

        
        serialzier = ProductSerialzier(product)
        return JsonResponse(
            {"data": {"product": serialzier.data, "related_product": data}, "errors":False, "message": ""}, safe=False
        )



def _sub_category_list(main_id):
    filter_super_category = MainCategory.objects.get(id=main_id).superCategory.pk 
    main_obj = MainCategory.objects.filter(superCategory__id=filter_super_category)
    data = []
    for i in main_obj:
        sub_category = SubCategory.objects.filter(mainCategory__id=i.pk)
        if sub_category is not None:
            for sub in sub_category:
                prod_count = len(Product.objects.filter(sub_category__id=sub.pk))
                data.append({
                     "sub_name": sub.sub_name,
                    "counts": prod_count,
                    "slug": sub.slug,
                    "pk": sub.pk,
                })
                if len(data) > 12:
                    return data 
    return data 


                

class CategoryProductViews(APIView):
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
        parameters=[ParemententCategorySerialzeir],
        responses=SuperCategoryStsSerializer
        
    )
    def get(self,request, types , slug):
        try:
            next = int(request.GET.get("page", 1))
            if types =='super':
                super_id = SuperCategory.objects.get(slug=slug).pk
                sub_category: bool = MainCategory.objects.filter(
                    superCategory__id=super_id
                ).exists()
                product_object = []
                if sub_category:
                    for main in MainCategory.objects.filter(superCategory__id=super_id):
                        prod_obj = Product.objects.filter(status=True, site_sts=True, main_category__id=main.pk)
                        serialzier = ProductListMiniSerilizers(prod_obj, many=True)
                        if len(prod_obj) > 0:
                            sub_names = main.main_name
                            if main.main_content is not None:
                                sub_names = main.main_content
                            if prod_obj is not None:
                                data = {
                                    "category": sub_names,
                                    "product": serialzier.data,
                                }
                                product_object.append(data)
                main = SuperCategory.objects.get(id=super_id)
                main_serialzier = SuperCategoryStsSerializer(main, many=False)
                return JsonResponse(
                    {
                        "data": {
                            "product": product_object,
                            "category": main_serialzier.data,
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if types =='main':
                main_id = MainCategory.objects.get(slug=slug).pk
                sub_category: bool = SubCategory.objects.filter(
                    mainCategory__id=main_id
                ).exists()
                product_object = []
                if sub_category:
                    for sub in SubCategory.objects.filter(mainCategory__id=main_id):
                        prod_obj = Product.objects.filter(status=True, site_sts=True, sub_category__id=sub.pk)
                        serialzeir = ProductListMiniSerilizers(prod_obj, may=True) 
                        if prod_obj is not None:
                            sub_names = sub.sub_name
                            data = {
                                "category": sub_names,
                                "product": serialzeir.data
                            }
                            product_object.append(data)
                main = MainCategory.objects.get(id=main_id)
                main_serialzier = MainCategortStsSerializer(main, many=False)
                return JsonResponse(
                    {
                        "data": {
                            "product": product_object,
                            "category": main_serialzier.data,
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if  types =='sub':
                sub_id = SubCategory.objects.get(slug=slug).pk
                limit = 30
                current = int(next) - 1
                product = Product.objects.filter(status=True, site_sts=True, sub_category__id=sub_id)[
                    current * limit : next * limit
                ]
                prod_serialzier = ProductListMiniSerilizers(product, many=True)
                count = product.count()
                pages = int(count / limit) + 1
                pagination = {
                    "pages": pages,
                    "current": current,
                    "next": next,
                    "limit": limit,
                    "count": count,
                }
                filter_prods = SubCategory.objects.get(id=sub_id)
                sub_data = _sub_category_list(main_id=filter_prods.mainCategory.pk)
                return JsonResponse(
                    {
                        "data": {
                            "product": prod_serialzier.data,
                            "pagination": pagination,
                            "filter_product": filter_prods.product_filter,
                            "sub_content": sub_data,
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            return JsonResponse(
                {"data": None, "errors": True, "message": "data not fount"}
            )
        except Exception as e:
            return JsonResponse({"data": None, "errors": True, "message": f"{e}"})
