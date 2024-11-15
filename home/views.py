from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Banner , HomePageCategory , CardImage
from .serialziers import BannerSerializers, HOmeSchemaSerialziers  , HomePageCategorySerialzier, ParementrHome, ResponseHOme , CardImageSerialziers
from product.models import Product
from product.serialzier import ProductListMiniSerilizers
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
# Create your views here.
from config.settings import site_name
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.views.decorators.vary import  vary_on_headers
from django.core.cache import cache

class BannerResponseSerialzier(serializers.Serializer):
    data = BannerSerializers()
    errors = serializers.BooleanField()
    message = serializers.CharField()




class BannerView(APIView):
    # @method_decorator(cache_page(60 * 60 * 10))
    # @method_decorator(vary_on_headers("Authorization"))
    # @extend_schema(
    #         responses=BannerResponseSerialzier
    # )
    def get(self, request, site):
        data = cache.get('home_banner')
        if site == "sts" and data is not None:
            return JsonResponse({"data": data, "errors": False, "message": ""}, safe=False)
        if site == "sts":
            banner = Banner.objects.filter(status=True, site_sts=True).order_by("id")
        if site == "rts":
            banner = Banner.objects.filter(status=True, site_rts=True).order_by("id")
        serialzier = BannerSerializers(banner , many=True)
        cache.set('home_banner', serialzier.data, timeout=60 * 60 * 10)
        return JsonResponse(
            {"data": serialzier.data, "errors": False, "message": ""}, safe=False
        )
    

class BannerDetailViews(APIView):
    # @method_decorator(cache_page(60 * 60 * 10))
    # @method_decorator(vary_on_headers("Authorization"))
    # @extend_schema(
    #         responses=BannerResponseSerialzier
    # )
    def get(self, request ,site, pk):
        if site == "sts":
            banner = Banner.objects.get(status=True,id=pk , site_sts=True)
            if banner.category is not None:
                product = Product.objects.filter(status=True, site_sts=True, main_category__id=banner.category.pk).order_by("-id")[:30]
        if site == "rts":
            banner = Banner.objects.get(status=True,id=pk, site_rts=True)
            if banner.category is not None:
                product = Product.objects.filter(status=True, main_category__id=banner.category.pk).order_by("-id")[:30]
        product_serializers = ProductListMiniSerilizers(product , many=True)
        serialzier = BannerSerializers(banner)
        return JsonResponse(
            {"data": {"banner": serialzier.data, "product": product_serializers.data}, "errors": True, "message": ""}, safe=False
        )

class HomePageCategoryView(APIView):
    # @method_decorator(cache_page(60 * 60 * 10))
    # @method_decorator(vary_on_headers("Authorization"))
    # @extend_schema(
    #         responses=ResponseHOme
    #         )
    def get(self, request, site):
        if site == "sts":
            data = cache.get('home_page')
            if data is not None:
                return JsonResponse(
                    {"data": data, "errors": True, "message": ""}, safe=False
                )
        data = []
        if site == "sts":
            home = HomePageCategory.objects.filter(status=True, site_sts=True).order_by("top")
        if site == "rts":
            home = HomePageCategory.objects.filter(status=True, site_rts=True).order_by("top")
        for i in home:
            if i.news:
                if site == "sts":
                    product = Product.objects.filter(status=True, news=True , site_sts=True)[:10]
                if site == "rts":
                    product = Product.objects.filter(status=True, news=True, site_rts=True)[:10]
                seriazlier = ProductListMiniSerilizers(product, many=True)
                cart_image = CardImage.objects.filter(status=True, homepagecategory__id=i.pk)
                cart_serialzier = CardImageSerialziers(cart_image, many=True)
                data.append(
                    {
                        "category_name": i.title,
                        "banner_image": i.cloudflare_id and (i.images_obj) or i.image and ( site_name + i.image.url ) or None,
                        "banner_image_url": i.image_url,
                        "product": cart_serialzier.data,
                        "product": seriazlier.data
                    }
                )
            if i.xitlar:
                if site == "sts":
                    product = Product.objects.filter(xitlar=True, status=True, site_sts=True)
                if site == "rts":
                    product = Product.objects.filter(xitlar=True, status=True, site_rts=True)

                prod_seriazlier = ProductListMiniSerilizers(product, many=True)
                cart_image = CardImage.objects.filter(status=True, homepagecategory__id=i.pk)
                cart_serialzier = CardImageSerialziers(cart_image, many=True)

                data.append(
                    {
                        "category_name": i.title,
                        "banner_image": i.cloudflare_id and (i.images_obj) or i.image and ( site_name + i.image.url ) or None,
                        "card_image": cart_serialzier.data,
                        "banner_image_url": i.image_url,
                        "product": prod_seriazlier.data
                    }
                )
                    

        
            if i.mainCategory is not None:
                if site == "sts":
                    product = Product.objects.filter(status=True, main_category__id=i.mainCategory.pk, site_sts=True)[:10]
                if site == "rts":
                    product = Product.objects.filter(status=True, main_category__id=i.mainCategory.pk)[:10]
                serialzier = ProductListMiniSerilizers(product, many=True)
                cart_image = CardImage.objects.filter(status=True, homepagecategory__id=i.pk)
                cart_serialzier = CardImageSerialziers(cart_image, many=True)
                data.append(
                    {
                        "category_name": i.title,
                        "banner_image": i.image and (i.images_obj ) or None,
                        "banner_image_url": i.image_url,
                        "card_image": cart_serialzier.data,
                        "product": serialzier.data
                    }
                )
        if cache.get('home_page') is None:
             cache.get_or_set('home_page', data, timeout=60*60*10)
        return JsonResponse({
            "data": data, "errors":False, "message": ""
        })




