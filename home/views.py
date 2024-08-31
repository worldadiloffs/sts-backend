from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Banner , HomePageCategory 
from .serialziers import BannerSerializers, HOmeSchemaSerialziers  , HomePageCategorySerialzier, ParementrHome, ResponseHOme
from product.models import Product
from product.serialzier import ProductListMiniSerilizers
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
# Create your views here.
from config.settings import site_name
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.views.decorators.vary import  vary_on_headers

class BannerResponseSerialzier(serializers.Serializer):
    data = BannerSerializers()
    errors = serializers.BooleanField()
    message = serializers.CharField()


class BannerView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
            responses=BannerResponseSerialzier
    )
    def get(self, request, site):
        if site == "sts":
            banner = Banner.objects.filter(status=True, site_sts=True).order_by("id")
        if site == "rts":
            banner = Banner.objects.filter(status=True, site_rts=True).order_by("id")
        serialzier = BannerSerializers(banner , many=True)
        return JsonResponse(
            {"data": serialzier.data, "errors": False, "message": ""}, safe=False
        )
    

class BannerDetailViews(APIView):
    @extend_schema(
            responses=BannerResponseSerialzier
    )
    def get(self, request ,site, pk):
        if site == "sts":
            banner = Banner.objects.get(status=True,id=pk , site_sts=True)
            if banner.category is not None:
                product = Product.objects.filter(status=True, site_sts=True, main_category__id=banner.category.pk).order_by("id")
        if site == "rts":
            banner = Banner.objects.get(status=True,id=pk, site_rts=True)
            if banner.category is not None:
                product = Product.objects.filter(status=True, site_rts=True, main_category__id=banner.category.pk).order_by("id")
        product_serializers = ProductListMiniSerilizers(product , many=True)
        serialzier = BannerSerializers(banner)
        return JsonResponse(
            {"data": {"banner": serialzier.data, "product": product_serializers.data}, "errors": True, "message": ""}, safe=False
        )
    
    



class HomePageCategoryView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
            responses=ResponseHOme
            )
    def get(self, request, site):
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
                data.append(
                    {
                        "category_name": i.title,
                        "banner_image": i.image and (site_name + i.image.url) or None,
                        "banner_image_url": i.image_url,
                        "product": seriazlier.data
                    }
                )
            if i.xitlar:
                if site == "sts":
                    product = Product.objects.filter(xitlar=True, status=True, site_sts=True)
                if site == "rts":
                    product = Product.objects.filter(xitlar=True, status=True, site_rts=True)

                prod_seriazlier = ProductListMiniSerilizers(product, many=True)

                data.append(
                    {
                        "category_name": i.title,
                        "banner_image": i.image and (site_name + i.image.url ) or None,
                        "banner_image_url": i.image_url,
                        "product": prod_seriazlier.data
                    }
                )
                    

        
            if i.mainCategory is not None:
                if site == "sts":
                    product = Product.objects.filter(status=True, main_category__id=i.mainCategory.pk, site_sts=True)[:10]
                if site == "rts":
                    product = Product.objects.filter(status=True, main_category__id=i.mainCategory.pk, site_rts=True)[:10]
                serialzier = ProductListMiniSerilizers(product, many=True)
                data.append(
                    {
                        "category_name": i.title,
                        "banner_image": i.image and (site_name + i.image.url ) or None,
                        "banner_image_url": i.image_url,
                        "product": serialzier.data
                    }
                )
        return JsonResponse({
            "data": data, "errors":False, "message": ""
        })



