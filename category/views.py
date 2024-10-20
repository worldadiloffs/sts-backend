from category.serializers import (
    CategoryHeaderSechema,
    CategorySchemaserialzeir,
    MainCategortStsMiniHomeSerializer,
    SuperCategoryStsMiniSerializer,
)
from .models import SuperCategory, MainCategory
from rest_framework.views import APIView
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page 
from django.views.decorators.vary import  vary_on_headers

class CategoryListJsonViews(APIView):
    @method_decorator(cache_page(60 * 60 * 6))
    # @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
        responses=CategorySchemaserialzeir
    )
    def get(self, request, site):
        if site == "sts":
            category = SuperCategory.objects.filter(status=True, sts_site=True).order_by("id")
        if site == "rts":
            category = SuperCategory.objects.filter(status=True, rts_site=True).order_by("id")
        serilalizer = SuperCategoryStsMiniSerializer(category, many=True)
        return JsonResponse(
            {"data": serilalizer.data, "errors": False, "message": ""}, safe=False
        )


class CategoryHeaderViews(APIView):
    @method_decorator(cache_page(60 * 60 * 6))
    # @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
            responses=CategoryHeaderSechema
    )
    def get(self, request, site):
        if site == "sts":
            main = MainCategory.objects.filter(sts_site=True, status=True, header_add=True).order_by("id")
            ommaobo_category = MainCategory.objects.filter(sts_site=True, status=True, ommabob=True).order_by("id")[:6]
        if site == "rts":
            ommaobo_category = MainCategory.objects.filter(rts_site=True, status=True, ommabob=True).order_by("id")[:6]
            main = MainCategory.objects.filter(rts_site=True, status=True, header_add=True).order_by("id")
        serialzier = MainCategortStsMiniHomeSerializer(main, many=True)

        ommabob_serialzier = MainCategortStsMiniHomeSerializer(
            ommaobo_category, many=True
        )

        return JsonResponse(
            {
                "data": {
                    "header_category": serialzier.data,
                    "ommabob_category": ommabob_serialzier.data,
                },
                "errors": False,
                "message": "",
            },
            safe=False,
        )