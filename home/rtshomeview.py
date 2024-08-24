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


class RTSBannerResponseSerialzier(serializers.Serializer):
    data = BannerSerializers()
    errors = serializers.BooleanField()
    message = serializers.CharField()


class RTSBannerView(APIView):
    @extend_schema(
            responses=RTSBannerResponseSerialzier
    )
    def get(self, request):
        banner = Banner.objects.filter(status=True,site_rts =True).order_by("id")
        serialzier = BannerSerializers(banner , many=True)
        return JsonResponse(
            {"data": serialzier.data, "errors": False, "message": ""}, safe=False
        )
    

class RTSBannerDetailViews(APIView):
    @extend_schema(
            responses=RTSBannerResponseSerialzier
    )
    def get(self, request , pk):
        banner = Banner.objects.get(status=True,id=pk , site_rts=True)
        if banner.category is not None:
            product = Product.objects.filter(status=True, site_rts=True, main_category__id=banner.category.pk).order_by("id")
            product_serializers =ProductListMiniSerilizers(product , many=True)
        serialzier = BannerSerializers(banner)
        return JsonResponse(
            {"data": {"banner": serialzier.data, "product": product_serializers.data}, "errors": True, "message": ""}, safe=False
        )
    
    



class RTSHomePageCategoryView(APIView):
    @extend_schema(
            responses=ResponseHOme
            )
    def get(self, request):
        data = []
        for i in HomePageCategory.objects.filter(status=True, site_rts=True).order_by("top"):
            if i.news:
                product = Product.objects.filter(status=True, news=True , site_rts=True)[:10]
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



