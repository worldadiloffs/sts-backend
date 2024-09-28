from rest_framework.views import APIView

from product.servisses import upload_image_to_cloudflare
from .serialzier import (
    ImagePostSeriazilizer,
    ProductListMiniSerilizers,
    ProductSerialzier,
)
from .models import Product, Image
from category.models import MainCategory, SubCategory, SuperCategory
from category.serializers import (
    MainCategortStsSerializer,
    SubCategoryMainiProductSerialzier,
    SuperCategoryStsSerializer,
)
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from drf_spectacular.utils import extend_schema


from rest_framework.parsers import MultiPartParser, FormParser

from django.db.models import Q
from settings.models import OrderSetting
from config.settings import site_name

from .serialzier import kredit_cal

from settings.models import MuddatliTolovxizmatlar
from django.core.cache import cache
import  io 


class ImageServis(APIView):
    def get(self, request):
        images = Image.objects.all()
        for i in images:
            if i.cloudflare_id is None and i.image is not None:
                cload_id = upload_image_to_cloudflare(i.image.file)
                i.cloudflare_id = cload_id
                i.save()
                
        return JsonResponse({"message": "Images uploaded to Cloudflare successfully."}, status=200)


class ProductDetailApiview(APIView):
    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, site, slug):
        main_category_product = None
        if site == "sts":
            product = Product.objects.get(slug=slug, status=True, site_sts=True)
            if product.main_category is not None:
                main_category_product = Product.objects.filter(
                    main_category__id=product.main_category.pk,
                    status=True,
                    site_sts=True,
                )[:10]
        if site == "rts":
            product = Product.objects.get(slug=slug, status=True, site_rts=True)
            if product.main_category is not None:
                main_category_product = Product.objects.filter(
                    main_category__id=product.main_category.pk,
                    status=True,
                    site_rts=True,
                )[:10]
        data = None
        if product.main_category is not None:
            if site == "sts":
                main_category_product = Product.objects.filter(
                    main_category__id=product.main_category.pk,
                    status=True,
                    site_sts=True,
                )[:10]
            if site == "rts":
                main_category_product = Product.objects.filter(
                    main_category__id=product.main_category.pk,
                    status=True,
                    site_rts=True,
                )[:10]

        if main_category_product is not None:
            main_serialzier = ProductListMiniSerilizers(
                main_category_product, many=True
            )
            data = main_serialzier.data
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
            }
        if product.super_category is not None and link_status:
            link = {
                "super": {
                    "name": product.super_category.super_name,
                    "slug": product.super_category.slug,
                },
            }

        serialzier = ProductSerialzier(product)
        muddat_tolov = []
        if product.price is not None:
            muddat = MuddatliTolovxizmatlar.objects.first()
            if muddat is not None:
                if site == "sts":
                    muddat_tolov_status = MuddatliTolovxizmatlar.objects.filter(
                        site_sts=True, status=True
                    )
                if site == "rts":
                    muddat_tolov_status = MuddatliTolovxizmatlar.objects.filter(
                        site_rts=True, status=True
                    )
                for i in muddat_tolov_status:
                    muddat_tolov.append(
                        {
                            "logo": i.logo and (site_name + i.logo.url) or None,
                            "name": i.name,
                            "oylar": i.kredit(product.price),
                        }
                    )
        return JsonResponse(
            {
                "data": {
                    "link": link,
                    "muddatli_tolov": muddat_tolov,
                    "product": serialzier.data,
                    "related_product": data,
                },
                "errors": False,
                "message": "",
            },
            safe=False,
            status=200,
        )


def _sub_category_list(main_id):
    filter_super_category = MainCategory.objects.get(id=main_id).superCategory.pk
    main_obj = MainCategory.objects.select_related('superCategory').filter(superCategory__id=filter_super_category)
    data = []
    for i in main_obj:
        sub_category = SubCategory.objects.select_related('mainCategory').filter(mainCategory__id=i.pk)
        if sub_category is not None:
            for sub in sub_category:
                prod_count = Product.objects.select_related('sub_category').filter(sub_category__id=sub.pk).count()
                data.append(
                    {
                        "sub_name": sub.sub_name,
                        "counts": prod_count,
                        "slug": sub.slug,
                        "pk": sub.pk,
                    }
                )
                if len(data) > 12:
                    return data
    return data


class SearchProductView(APIView):
    def get(self, request, site):
        search = request.GET.get("search", "")
        next = int(request.GET.get("page", 1))
        limit = 12
        current = int(next) - 1
        if site == "sts":
            count = len(
                Product.objects.filter(status=True, site_sts=True)
                .filter(Q(product_name__icontains=search))
            )
            product = (
                Product.objects.filter(status=True, site_sts=True)
                .filter(Q(product_name__icontains=search))
                [current * limit : next * limit]
            )
        if site == "rts":
            count = (
                Product.objects.filter(status=True, site_rts=True)
                .filter(Q(product_name__icontains=search))
                .count()
            )
            product = (
                Product.objects.filter(status=True, site_rts=True)
                .filter(Q(product_name__icontains=search))
                [current * limit : next * limit]
            )

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
            {
                "data": {"product": serializer.data, "pagination": pagination},
                "errors": False,
                "message": "",
            },
            safe=False,
        )




class CartProductApiview(APIView):
    def post(self, request, site):
        products = request.data.get("products", None)
        doller_obj = OrderSetting.objects.first()
        doller = doller_obj.doller * 1.12

        data = []
        try:
            if products is not None:
                for product in products:
                    product_obj = Product.objects.get(id=product["id"])
                    obj = {
                        "checked": product["checked"],
                        "count": product.get("count"),
                        "counts": product.get("counts"),
                        "id": product_obj.pk,
                        "image": product_obj.image
                        and (site_name + product_obj.image)
                        or None,
                        "price": int(product_obj.price * doller),
                        "product_name": product_obj.product_name,
                        "product_video": product_obj.product_video
                        and (site_name + product_obj.product_video.url)
                        or None,
                        "slug": product_obj.slug,
                        "tavar_dagavornaya": product_obj.tavar_dagavornaya,
                        "kredit_summa": int(
                            kredit_cal(price=product_obj.price, oy=12, foiz=36)
                        ),
                        "discount_price": int(
                            product_obj.discount_price
                            and int(product_obj.discount_price * doller)
                            or int((product_obj.price * doller) * 1.2)
                        ),
                    }
                    data.append(obj)
                return JsonResponse(
                    {"data": data, "errors": False, "message": ""}, safe=False
                )
        except Exception as e:
            return JsonResponse(
                {"data": None, "errors": True, "message": str(e)}, safe=False
            )




class CategoryProductViews(APIView):
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
        # parameters=[ParemententCategorySerialzeir],
        responses=SuperCategoryStsSerializer
    )
    def get(self, request,site, types, slug):
        try:
            next = int(request.GET.get("page", 1))
            min_price = request.GET.get("min_price", None)
            max_price = request.GET.get("max_price", None)
            order_py = str(request.GET.get("order_by", "-id"))
            avalable = request.GET.get("avalable", False)
            if types == "super":
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
                        prod_obj = Product.objects.filter(
                            status=True, main_category__id=main.pk
                        )[:5]
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
                            "link": {"super": {"name": name, "slug": super_slug}},
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if types == "main":
                main_objs = MainCategory.objects.get(slug=slug)
                main_id = main_objs.pk
                sub_category: bool = SubCategory.objects.filter(
                    mainCategory__id=main_id
                ).exists()
                product_object = []
                if sub_category:
                    for sub in SubCategory.objects.filter(mainCategory__id=main_id):
                        prod_obj = Product.objects.select_related('sub_category').filter(
                            status=True,  sub_category__id=sub.pk
                        )[:5]
                        serialzeir = ProductListMiniSerilizers(prod_obj, many=True)
                        if len(prod_obj) > 0:
                            if prod_obj is not None:
                                sub_names = sub.sub_name
                                data = {
                                    "category": sub_names,
                                    "product": serialzeir.data,
                                }
                                product_object.append(data)
                main_serialzier = MainCategortStsSerializer(main_objs)
                return JsonResponse(
                    {
                        "data": {
                            "name": main_objs.main_name,
                            "product": product_object,
                            "category": main_serialzier.data,
                            "link": {
                                "super": {
                                    "name": main_objs.superCategory.super_name,
                                    "slug": main_objs.superCategory.slug,
                                },
                                "main": {
                                    "id": main_objs.pk,
                                    "name": main_objs.main_name,
                                    "slug": main_objs.slug,
                                },
                            },
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if types == "sub":
                filter_prods = SubCategory.objects.get(slug=slug)
                sub_id = filter_prods.pk
                limit = 12
                current = int(next) - 1
                if (
                    min_price is not None
                    and max_price is not None
                    and min_price
                    and max_price
                ):  
                    orders_settings = cache.get_or_set('doller', OrderSetting.objects.first().get_doller_funtion, timeout=60*15)
                    min_price = int(min_price) / orders_settings
                    max_price = int(max_price) / orders_settings
                    if avalable:
                        count = Product.objects.select_related('sub_category').filter(
                            status=True,
                            sub_category__id=sub_id,
                            price__range=(min_price, max_price),
                            available=True,
                        ).count()
                        product = Product.objects.filter(
                            status=True,
                            sub_category__id=sub_id,
                            price__range=(min_price, max_price),
                            available=True,
                        ).order_by(order_py)[current * limit : next * limit]
                    count = Product.objects.select_related('sub_category').filter(
                        status=True,
                        sub_category__id=sub_id,
                        price__range=(min_price, max_price),
                    ).count()
                    product = Product.objects.filter(
                        status=True,
                        sub_category__id=sub_id,
                        price__range=(min_price, max_price),
                    ).order_by(order_py)[current * limit : next * limit]
                else:
                    if avalable:
                        count = Product.objects.filter(
                            status=True,
                            sub_category__id=sub_id,
                            available=True,
                        ).count()

                        product = Product.objects.filter(
                            status=True,
                            sub_category__id=sub_id,
                            available=True,
                        ).order_by(order_py)[current * limit : next * limit]
                    count = Product.objects.filter(
                        status=True,  sub_category__id=sub_id
                    ).count()
                    product = Product.objects.filter(
                        status=True, sub_category__id=sub_id
                    ).order_by(order_py)[current * limit : next * limit]
                prod_serialzier = ProductListMiniSerilizers(product, many=True)

                pages = int(count / limit) + 1
                pagination = {
                    "count": count,
                    "pages": pages,
                    "current": current,
                    "next": next,
                    "limit": limit,
                }
                sub_data = _sub_category_list(main_id=filter_prods.mainCategory.pk)
                filter_category = SubCategory.objects.filter(
                    mainCategory__id=filter_prods.mainCategory.pk
                )
                filter_serialzier = SubCategoryMainiProductSerialzier(
                    filter_category, many=True
                )
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
                            "sub_content": sub_data,
                            "filter_category": filter_serialzier.data,
                            "link": links,
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
