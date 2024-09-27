from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db.models import Q, Prefetch
from drf_spectacular.utils import extend_schema

from category.serializers import   SuperCategoryStsSerializer, MainCategortStsSerializer, SubCategoryMainiProductSerialzier
from .serialzier import (
    ProductListMiniSerilizers
)
from .models import SuperCategory, MainCategory, SubCategory, Product
from settings.models import OrderSetting, MuddatliTolovxizmatlar

class CategoryProductViewss(APIView):
    @extend_schema(
        responses=SuperCategoryStsSerializer
    )
    def get(self, request, site, types, slug):
        try:
            # Extract and validate query parameters
            page = int(request.GET.get("page", 1))
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            order_by = request.GET.get("order_by", "-id")
            available = request.GET.get("available", "false").lower() == "true"
            limit = 12
            offset = (page - 1) * limit

            if types == "super":
                return self.handle_super_category(site, slug)
            elif types == "main":
                return self.handle_main_category(site, slug)
            elif types == "sub":
                return self.handle_sub_category(site, slug, page, limit, order_by, min_price, max_price, available)
            else:
                return Response(
                    {"data": None, "errors": True, "message": "Invalid type specified."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"data": None, "errors": True, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_super_category(self, site, slug):
        super_category = get_object_or_404(SuperCategory, slug=slug)
        main_categories = MainCategory.objects.filter(superCategory=super_category)
        
        product_object = []
        for main in main_categories.prefetch_related(
            Prefetch('product_set', queryset=Product.objects.filter(status=True, **self.get_site_filter(site)).only('id', 'product_name', 'price')[:5])
        ):
            products = main.product_set.all()
            if products:
                sub_name = main.main_content or main.main_name
                serialized_products = ProductListMiniSerilizers(products, many=True).data
                product_object.append({
                    "category": sub_name,
                    "product": serialized_products,
                })

        serialized_super = SuperCategoryStsSerializer(super_category)

        return Response(
            {
                "data": {
                    "name": super_category.super_name,
                    "product": product_object,
                    "category": serialized_super.data,
                    "link": {"super": {"name": super_category.super_name, "slug": super_category.slug}},
                },
                "errors": False,
                "message": "",
            },
            status=status.HTTP_200_OK
        )

    def handle_main_category(self, site, slug):
        main_category = get_object_or_404(MainCategory, slug=slug)
        sub_categories = SubCategory.objects.filter(mainCategory=main_category)
        
        product_object = []
        for sub in sub_categories.prefetch_related(
            Prefetch('product_set', queryset=Product.objects.filter(status=True, **self.get_site_filter(site)).only('id', 'product_name', 'price')[:5])
        ):
            products = sub.product_set.all()
            if products:
                serialized_products = ProductListMiniSerilizers(products, many=True).data
                product_object.append({
                    "category": sub.sub_name,
                    "product": serialized_products,
                })

        serialized_main = MainCategortStsSerializer(main_category)

        return Response(
            {
                "data": {
                    "name": main_category.main_name,
                    "product": product_object,
                    "category": serialized_main.data,
                    "link": {
                        "super": {
                            "name": main_category.superCategory.super_name,
                            "slug": main_category.superCategory.slug,
                        },
                        "main": {
                            "id": main_category.pk,
                            "name": main_category.main_name,
                            "slug": main_category.slug,
                        },
                    },
                },
                "errors": False,
                "message": "",
            },
            status=status.HTTP_200_OK
        )

    def handle_sub_category(self, site, slug, page, limit, order_by, min_price, max_price, available):
        sub_category = get_object_or_404(SubCategory, slug=slug)
        products_query = Product.objects.filter(status=True, sub_category=sub_category)

        # Apply site filter
        products_query = products_query.filter(**self.get_site_filter(site))

        # Apply price range if provided
        if min_price and max_price:
            doller = self.get_dollar_rate()
            try:
                min_price = float(min_price) / doller
                max_price = float(max_price) / doller
                products_query = products_query.filter(price__range=(min_price, max_price))
            except ValueError:
                pass  # Handle invalid price inputs if necessary

        # Apply availability filter
        if available:
            products_query = products_query.filter(available=True)

        # Order the products
        products_query = products_query.order_by(order_by)

        # Pagination
        offset =  (page - 1) * limit
        total_count = products_query.count()
        products = products_query.select_related('sub_category').prefetch_related('image_set')[
            offset:offset + limit
        ]

        serialized_products = ProductListMiniSerilizers(products, many=True).data

        # Calculate pagination details
        total_pages = (total_count + limit - 1) // limit  # Ceiling division

        # Fetch sub category list with caching
        sub_data = cache.get_or_set(
            f"sub_category_list_{sub_category.mainCategory.pk}",
            lambda: self._sub_category_list(sub_category.mainCategory.pk),
            timeout=60*15
        )

        # Serialize filter categories
        filter_categories = SubCategory.objects.filter(mainCategory=sub_category.mainCategory)
        serialized_filters = SubCategoryMainiProductSerialzier(filter_categories, many=True).data

        # Construct links
        links = {
            "super": {
                "name": sub_category.mainCategory.superCategory.super_name,
                "slug": sub_category.mainCategory.superCategory.slug,
            },
            "main": {
                "name": sub_category.mainCategory.main_name,
                "slug": sub_category.mainCategory.slug,
            },
            "sub": {
                "name": sub_category.sub_name,
                "slug": sub_category.slug
            },
        }

        return Response(
            {
                "data": {
                    "name": sub_category.sub_name,
                    "product": serialized_products,
                    "pagination": {
                        "count": total_count,
                        "pages": total_pages,
                        "current": page,
                        "next": page + 1 if page < total_pages else None,
                        "limit": limit,
                    },
                    "sub_content": sub_data,
                    "filter_category": serialized_filters,
                    "link": links,
                },
                "errors": False,
                "message": "",
            },
            status=status.HTTP_200_OK
        )

    def _sub_category_list(self, main_id):
        main_category = get_object_or_404(MainCategory, id=main_id)
        super_category_id = main_category.superCategory.pk
        sub_categories = SubCategory.objects.filter(mainCategory__superCategory__id=super_category_id).select_related('mainCategory')

        data = []
        for sub in sub_categories:
            product_count = sub.product_set.filter(status=True).count()
            data.append({
                "sub_name": sub.sub_name,
                "counts": product_count,
                "slug": sub.slug,
                "pk": sub.pk,
            })
            if len(data) >= 12:
                break
        return data

    def get_site_filter(self, site):
        if site == "sts":
            return {"site_sts": True}
        elif site == "rts":
            return {"site_rts": True}
        else:
            raise ValueError("Invalid site value provided.")

    def get_dollar_rate(self):
        # Utilize caching to store the dollar rate
        return cache.get_or_set(
            'dollar_rate',
            lambda: OrderSetting.objects.first().get_doller_funtion(),
            timeout=60*15
        )
