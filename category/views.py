from django.shortcuts import render

from category.serializers import (
    MainCategortStsMiniHomeSerializer,
    SuperCategoryStsMiniSerializer,
    SuperCategoryStsSerializer,
)
from .models import SuperCategory, MainCategory, SubCategory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http import JsonResponse


class SuperCategoryListViews(ListAPIView):
    # queryset = SuperCategory.objects.all()
    serializer_class = SuperCategoryStsSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        queryset = SuperCategory.objects.filter(sts_site=False).order_by("?")
        return queryset


class CategoryListJsonViews(APIView):
    def get(self, request):
        category = SuperCategory.objects.filter(status=True, sts_site=True).order_by(
            "?"
        )
        serilalizer = SuperCategoryStsMiniSerializer(category, many=True)
        return JsonResponse(
            {"data": serilalizer.data, "errors": False, "message": ""}, safe=False
        )


class MainCategoryViews(APIView):
    def get(self, request):
        main = MainCategory.objects.filter(
            sts_site=True, status=True, header_add=True
        ).order_by("id")
        serialzier = MainCategortStsMiniHomeSerializer(main, many=True)
        ommaobo_category = MainCategory.objects.filter(
            sts_site=True, status=True, ommabob=True
        ).order_by("id")[:5]
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
