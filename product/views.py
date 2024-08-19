from rest_framework.views import APIView
from .serialzier import ImagePostSeriazilizer, ParemententCategorySerialzeir, ProductDetailSerialzeir, ProductListMiniSerilizers , ProductSerialzier , ImageSeriazilizer
from .models import Product , Image
from category.models import MainCategory, SubCategory, SuperCategory
from category.serializers import (
    MainCategortStsSerializer,
    SubCategoryMainiProductSerialzier,
    SubCategoryStsSerialzier,
    SuperCategoryStsSerializer,
)
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from drf_spectacular.utils import extend_schema


from rest_framework.parsers import MultiPartParser , FormParser

from django.db.models import Q 
from settings.models import OrderSetting
from config.settings import site_name




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
            main_category_product = Product.objects.filter(main_category__id=product.main_category.pk, status=True, site_sts=True)[:10]
            main_serialzier = ProductListMiniSerilizers(main_category_product, many=True)
            data = main_serialzier.data 
            # link = get_link(product.super_category , product.main_category, product.sub_category)
        
        link_status = True
        if product.sub_category is not None:
            link_status = False
            link = {
                "super": {
                    "name": product.super_category.super_name,
                    "slug": product.super_category.slug,
                },
                "main": {
                    "name": product.main_category.main_name,
                    "slug": product.main_category.slug,
                },
                "sub": {
                    "name": product.sub_category.sub_name,
                    "slug": product.sub_category.slug,
                },
            }
        if product.main_category is not None and link_status:
            link_status =False
            link = {
                "super": {
                    "name": product.super_category.super_name,
                    "slug": product.super_category.slug,
                },
                "main": {
                    "name": product.main_category.main_name,
                    "slug": product.main_category.slug,
                },
            }
        if product.super_category is not None and link_status:
            link = {
                "super": {
                    "name": product.super_category.super_name,
                    "slug": product.super_category.slug,
                },
            }
           
        serialzier = ProductSerialzier(product)
        
              
        return JsonResponse(
                {"data": {"link": link, "product": serialzier.data, "related_product": data }, "errors":False, "message": ""}, safe=False
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



class SearchProductView(APIView):
    def get(self, request):
        search = request.GET.get("search", "")
        if search:
            pass 
        next = int(request.GET.get("page", 1))
        limit = 12
        current = int(next) - 1
        count = Product.objects.filter(status=True, site_sts=True).count()
        product = Product.objects.filter(status=True, site_sts=True).filter(Q(product_name__icontains=search)).order_by("id")[
                    current * limit : next * limit
                ]
        # count = product.count()
        pages = int(count / limit) + 1
        pagination = {
                    "count": count,
                    "pages": pages,
                    "current": current,
                    "next": next,
                    "limit": limit,
                }
        serializer = ProductListMiniSerilizers(product, many=True)
        return JsonResponse(
            {"data": {"product": serializer.data, "pagination": pagination}, "errors": False, "message": ""}, safe=False
        )    


class CartProductApiview(APIView):
    def post(self, request):
        products = request.data.get("products", None)
        doller_obj = OrderSetting.objects.first()
        doller = doller_obj.doller * 1.12
        data = []
        try:
            if products is not None:
                for product in products:
                    product_obj = Product.objects.get(id=product["id"])
                    obj = {
                        "checked": product['checked'],
                        "count": product.get('count'),
                        "counts": product.get('counts'),
                        "id": product_obj.pk,
                        "image": product_obj.image and (site_name + product_obj.image)  or None,
                        "price": int(product_obj.price * doller),
                        "product_name": product_obj.product_name,
                        "product_video": product_obj.product_video  and (site_name + product_obj.product_video.url)  or None,
                        "slug": product_obj.slug,
                        "tavar_dagavornaya": product_obj.tavar_dagavornaya
                        }
                    data.append(obj)
                return JsonResponse({"data": data, "errors": False, "message": ""}, safe=False)
        except Exception as e:
            return JsonResponse({"data": None, "errors": True, "message": str(e)}, safe=False)                  



def _product_filter(product_list, min_price, max_price, yangi, ommab):
    pass 
    

class CategoryProductViews(APIView):
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
        # parameters=[ParemententCategorySerialzeir],
        responses=SuperCategoryStsSerializer
        
    )
    def get(self,request, types , slug):
        try:
            next = int(request.GET.get("page", 1))
            min_price = request.GET.get("min_price",None)
            max_price = request.GET.get("max_price", None)
            yangi  = request.GET.get("yangi", False)
            ommabob = request.GET.get("ommabob", False)
            qimmatroq = request.GET.get("qimmatroq", False)
            chegirma = request.GET.get("chegirma", False)
            order_py = request.GET.get("order_py", None)
            if order_py is not None or '':
                order_py = 'id'
            avalable = request.GET.get("avalable", False)
            if types =='super':
                supers = SuperCategory.objects.get(slug=slug)
                super_id = supers.pk
                name = supers.super_name
                super_slug = supers.slug
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
                            "name": main.super_name,
                            "product": product_object,
                            "category": main_serialzier.data,
                            "link": {"super":{"name":name, "slug": super_slug}}
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if types =='main':
                main_objs = MainCategory.objects.get(slug=slug)
                main_id = main_objs.pk

                sub_category: bool = SubCategory.objects.filter(
                    mainCategory__id=main_id
                ).exists()
                product_object = []
                if sub_category:
                    for sub in SubCategory.objects.filter(mainCategory__id=main_id):
                        prod_obj = Product.objects.filter(status=True, site_sts=True, sub_category__id=sub.pk)
                        serialzeir = ProductListMiniSerilizers(prod_obj, many=True) 
                        if len(prod_obj) > 0:
                            if prod_obj is not None:
                                sub_names = sub.sub_name
                                data = {
                                    "category": sub_names,
                                    "product": serialzeir.data
                                }
                                product_object.append(data) 
                main = MainCategory.objects.get(id=main_id)
                main_serialzier = MainCategortStsSerializer(main)
                return JsonResponse(
                    {
                        "data": {
                            "name": main_objs.main_name,
                            "product": product_object,
                            "category": main_serialzier.data,
                            "link": {
                                "super": {"name": main_objs.superCategory.super_name, "slug": main_objs.superCategory.slug},
                                "main":{ "id": main_objs.pk, "name":main_objs.main_name, "slug": main_objs.slug}}
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if  types =='sub':
                sub_id = SubCategory.objects.get(slug=slug).pk
                limit = 12
                current = int(next) - 1
                if min_price is not None and max_price is not None and min_price and max_price:
                    min_price = int(min_price)/ OrderSetting.objects.first().doller
                    max_price = int(max_price) / OrderSetting.objects.first().doller
                    if avalable:
                        count = Product.objects.filter(
                            status=True,
                            site_sts=True,
                            sub_category__id=sub_id,
                            price__range=(min_price, max_price),
                            available=True,
                        ).count()
                        product = Product.objects.filter(
                            status=True,
                            site_sts=True,
                            sub_category__id=sub_id,
                            price__range=(min_price, max_price),
                            available=True,
                        ).order_by(order_py)[current * limit : next * limit]
                    count = Product.objects.filter(
                        status=True,
                        site_sts=True,
                        sub_category__id=sub_id,
                        price__range=(min_price, max_price),
                    ).count()
                    product = Product.objects.filter(
                        status=True,
                        site_sts=True,
                        sub_category__id=sub_id,
                        price__range=(min_price, max_price),
                    ).order_by(order_py)[ current * limit : next * limit]
                else:
                    if avalable:
                        count = Product.objects.filter(
                            status=True,
                            site_sts=True,
                            sub_category__id=sub_id,
                            available=True,
                        ).count()

                        product = Product.objects.filter(
                            status=True,
                            site_sts=True,
                            sub_category__id=sub_id,
                            available=True,
                        ).order_by(order_py)[current * limit : next * limit]
                    count = Product.objects.filter(status=True, site_sts=True, sub_category__id=sub_id).count()
                    product = Product.objects.filter(status=True, site_sts=True, sub_category__id=sub_id).order_by(order_py)[
                        current * limit : next * limit
                    ]
                
                
                # count =  Product.objects.filter(status=True, site_sts=True, sub_category__id=sub_id).count()
                # product = Product.objects.filter(status=True, site_sts=True, sub_category__id=sub_id)[
                #     current * limit : next * limit
                # ]
                prod_serialzier = ProductListMiniSerilizers(product, many=True)
           
                pages = int(count / limit) + 1
                pagination = {
                    "count": count,
                    "pages": pages,
                    "current": current,
                    "next": next,
                    "limit": limit,
                }
                filter_prods = SubCategory.objects.get(id=sub_id)
                sub_data = _sub_category_list(main_id=filter_prods.mainCategory.pk)
                filter_category = SubCategory.objects.filter(mainCategory__id=filter_prods.mainCategory.pk)
                filter_serialzier = SubCategoryMainiProductSerialzier(filter_category, many=True)
                links = {
                    "super": {
                        "name": filter_prods.mainCategory.superCategory.super_name,
                        "slug": filter_prods.mainCategory.superCategory.slug,
                    },
                    "main": {
                        "name": filter_prods.mainCategory.main_name,
                        "slug": filter_prods.mainCategory.slug,
                    },
                    "sub": {"name": filter_prods.sub_name, "slug": filter_prods.slug},
                }
                return JsonResponse(
                    {
                        "data": {
                            "name": filter_prods.sub_name,
                            "product": prod_serialzier.data,
                            "pagination": pagination,
                            "filter_product": filter_prods.product_filter,
                            "sub_content": sub_data,
                            "filter_category": filter_serialzier.data,
                            "link": links
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
