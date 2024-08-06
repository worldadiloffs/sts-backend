from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Banner , HomePageCategory , homePage
from .serialziers import BannerSerializers , HomePageSerializers , HomePageCategorySerialzier
from product.models import Product
from product.serialzier import ProductListMiniSerilizers

# Create your views here.


class BannerView(APIView):
    def get(self, request):
        banner = Banner.objects.filter(status=True, site_sts=True).order_by("id")
        serialzier = BannerSerializers(banner , many=True)
        return JsonResponse(
            {"data": serialzier.data, "errors": True, "message": ""}, safe=False
        )
    



class HomePageCategoryView(APIView):
    def get(self, request):
        data = []
        for i in HomePageCategory.objects.filter(status=True, site_sts=True).order_by('top'):
            if i.news:
                product = Product.objects.filter(status=True, news=True , site_sts=True)[:10]
                seriazlier = ProductListMiniSerilizers(product, many=True)
                data.append(
                    {
                        "category_name": i.title,
                        "image": i.image and i.image.url or None,
                        "image_url": i.image_url,
                        "product": seriazlier.data
                    }
                )
            if i.xitlar:
                product = Product.objects.filter(xitlar=True, status=True, site_sts=True)
                prod_seriazlier = ProductListMiniSerilizers(product, many=True)
                data.append(
                    {
                        "category_name": i.title,
                        "image": i.image and i.image.url or None,
                        "image_url": i.image_url,
                        "product": prod_seriazlier.data
                    }
                )
            if i.mainCategory is not None:
                product = Product.objects.filter(status=True, main_category__id=i.mainCategory.pk, site_sts=True)[:10]
                serialzier = ProductListMiniSerilizers(product, many=True)
                data.append(
                    {
                        "category_name": i.title,
                        "image": i.image and i.image.url or None,
                        "image_url": i.image_url,
                        "product": serialzier.data
                    }
                )
        return JsonResponse({
            "data": data, "errors":True, "message": ""
        })



