from django.shortcuts import render

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


# class SuperCategoryListViews(ListAPIView):
#     # queryset = SuperCategory.objects.all()
#     serializer_class = SuperCategoryStsSerializer
#     lookup_field = "slug"
#     lookup_url_kwarg = "slug"

#     def get_queryset(self):
#         queryset = SuperCategory.objects.filter(sts_site=False).order_by("?")
#         return queryset



class RTSCategoryListJsonViews(APIView):
    @extend_schema(
        responses=CategorySchemaserialzeir
    )
    def get(self, request):
        category = SuperCategory.objects.filter(status=True, rts_site=True).order_by(
            "id"
        )
        serilalizer = SuperCategoryStsMiniSerializer(category, many=True)
        return JsonResponse(
            {"data": serilalizer.data, "errors": False, "message": ""}, safe=False
        )


class RTSCategoryHeaderViews(APIView):
    @extend_schema(
            responses=CategoryHeaderSechema
    )
    def get(self, request):
        main = MainCategory.objects.filter(
            rts_site=True, status=True, header_add=True
        ).order_by("id")
        serialzier = MainCategortStsMiniHomeSerializer(main, many=True)
        ommaobo_category = MainCategory.objects.filter(
            rts_site=True, status=True, ommabob=True
        ).order_by("id")[:6]
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



