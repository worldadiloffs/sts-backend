from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serialzier import ProductListMiniSerilizers, ProductSerialzier
from .models import Product
from category.models import MainCategory, SubCategory, SuperCategory
from category.serializers import (
    MainCategortStsSerializer,
    SuperCategoryStsSerializer,
    SubCategoryStsSerialzier,
)
from django.http import JsonResponse


class ProductListMiniView(APIView):
    def get(self, request):
        product = Product.objects.all()
        seriazleir = ProductListMiniSerilizers(product, many=True)
        return JsonResponse(
            {"data": seriazleir.data, "errors": False, "message": ""}, safe=False
        )
    



def _sub_category_list(sub_id):
    filter_sub_category = SubCategory.objects.get(id=sub_id)
    filter_main_category = MainCategory.objects.get(id=filter_sub_category.mainCategory.pk).superCategory.pk 
    main_obj = MainCategory.objects.filter(superCategory__id=filter_main_category)
    data = []
    for i in main_obj:
        sub_category = SubCategory.objects.filter(mainCategory__id=i.pk)
        if sub_category is not None:
            for sub in sub_category:
                prod_count = len(Product.objects.filter(sub_category__id=sub.pk))
                data({
                     "sub_name": sub.sub_name,
                    "counts": prod_count,
                    "slug": sub.slug,
                    "pk": sub.pk,
                })

    return data 
                


        


    
    


class CategoryProductViews(APIView):
    def get(self, request):
        try:
            super_id = request.GET.get("super_id")
            main_id = request.GET.get("main_id")
            sub_id = request.GET.get("sub_id")
            next = int(request.GET.get("page", 1))
            if super_id is not None:
                sub_category: bool = MainCategory.objects.filter(
                    superCategory__id=super_id
                ).exists()
                product_object = []
                if sub_category:
                    for main in MainCategory.objects.filter(superCategory__id=super_id):
                        prod_obj = list(
                            Product.objects.filter(main_category__id=main.pk)
                            .values()
                            .order_by("id")
                        )
                        if len(prod_obj) > 0:
                            sub_names = main.main_name
                            if prod_obj is not None:
                                data = {
                                    "main_category_name": sub_names,
                                    "product": prod_obj,
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
            if main_id is not None:
                sub_category: bool = SubCategory.objects.filter(
                    mainCategory__id=main_id
                ).exists()
                product_object = []
                if sub_category:
                    for sub in SubCategory.objects.filter(mainCategory__id=main_id):
                        prod_obj = list(
                            Product.objects.filter(sub_category__id=sub.pk)
                            .values()
                            .order_by("id")
                        )
                        if len(prod_obj) > 0:
                            sub_names = sub.sub_name
                            if prod_obj is not None:
                                data = {
                                    "sub_category_name": sub_names,
                                    "product": prod_obj,
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
            if sub_id is not None:
                limit = 30
                current = int(next) - 1
                product = Product.objects.filter(sub_category__id=sub_id)[
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
                sub_data = _sub_category_list(sub_id=sub_id)
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
