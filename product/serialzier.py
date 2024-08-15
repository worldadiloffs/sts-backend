from rest_framework import serializers
from .models import Product, Image
from config.settings import site_name
from settings.models import OrderSetting
from category.serializers import (
    SuperCategoryStsMiniSerializer,
    MainCategortStsMiniSerializer,
    SubCategoryStsMiniSerialzier,
)


class ImageSeriazilizer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = "__all__"

    def get_image(self, obj):
        image = obj.image
        if image:
            return site_name + image.url

        return None


class ImagePostSeriazilizer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


def doller_funtion():
    order = OrderSetting.objects.first()
    return order.doller * 1.12 # 1.12 is for dollar exchange rate


class ProductSerialzier(serializers.ModelSerializer):
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    category = serializers.SerializerMethodField()
    # main_category = serializers.SerializerMethodField()
    # sub_category = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_price(self, obj):
        return obj.price and obj.price * doller_funtion() or 0

    # def get_super_category(self, obj):
    #     category = obj.super_category
    #     if category is not None:
    #         return {
    #             "id": category.id,
    #             "category_name": category.super_name,
    #             "slug": category.slug
    #         }

    # def get_main_category(self, obj):
    #     category = obj.main_category
    #     super_category = obj.super_category
    #     if category is not None:
    #         return {
    #             "super":{"id": super_category.id, "cateogry_name": super_category.super_name, "slug": super_category.slug},
    #             "main":{"id": category.id , "category_name": category.main_name, "slug": category.slug}
    #         }

    def get_category(self, obj):
        sub_category = obj.sub_category
        super_category = obj.super_category
        main_category = obj.main_category
        if sub_category is not None:
            return  {
                    "id": super_category.id,
                    "cateogry_name": super_category.super_name,
                    "slug": super_category.slug,
                    "children": {
                        "id": main_category.id,
                        "category_name": main_category.main_name,
                        "slug": main_category.slug,
                        "children": {
                            "id": sub_category.id,
                            "category_name": sub_category.sub_name,
                            "slug": sub_category.slug,
                        },
                    },
                },
            
        if main_category is not None:
            return  {
                    "id": super_category.id,
                    "name": super_category.super_name,
                    "slug": super_category.slug,
                    "children": {
                        "id": main_category.id,
                        "name": main_category.main_name,
                        "slug": main_category.slug,
                    },
                },
            

        if super_category is not None:
            return {
                "id": super_category.id,
                "cateogry_name": super_category.super_name,
                "slug": super_category.slug,
                "children": {},
            }


class ProductDetailSerialzeir(serializers.ModelSerializer):
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    super_category = serializers.SerializerMethodField()
    main_category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "main_category",
            "super_category",
            "sub_category",
            "images",
            "product_video",
            "slug",
            "price",
            "discount_price",
            "short_content",
            "tavar_dagavornaya",
            "counts",
        )

    def get_price(self, obj):
        return obj.price and obj.price * doller_funtion() or obj.price

    def get_super_category(self, obj):
        category = obj.super_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.super_name,
                "slug": category.slug,
            }

    def get_main_category(self, obj):
        category = obj.main_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.main_name,
                "slug": category.slug,
            }

    def get_sub_category(self, obj):
        category = obj.sub_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.sub_name,
                "slug": category.slug,
            }


class ProductListMiniSerilizers(serializers.ModelSerializer):
    # images = ImageSeriazilizer(required=False, read_only=True, many=True)
    image = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "category_name",
            "image",
            "product_video",
            "slug",
            "price",
            "discount_price",
            "short_content",
            "tavar_dagavornaya",
            "counts",
            "super_category",
        )

    def get_price(self, obj):
        return obj.price and obj.price * doller_funtion() or 0

    def get_image(self, obj):
        image = obj.image
        if image:
            return site_name + image
        return None

    def get_category_name(self, obj):
        category = obj.super_category
        if category is not None:
            return category.super_name


class ParemententCategorySerialzeir(serializers.Serializer):
    super_id = serializers.IntegerField(required=False)
    main_id = serializers.IntegerField(required=False)
    sub_id = serializers.IntegerField(required=False)
