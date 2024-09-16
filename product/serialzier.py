from rest_framework import serializers
from cashback.views import cashback_values
from .models import Product, Image
from config.settings import site_name
from settings.models import OrderSetting

from django.core.cache import cache
from .servisses import get_image_url_from_cloudflare 

class ImageSeriazilizer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = "__all__"

    def get_image(self, obj):
        # if obj.cloudflare_id:
        #     return get_image_url_from_cloudflare(obj.cloudflare_id, variant="mobile")
        image = obj.image
        if image:
            return site_name + image.url
        return None
    

    



    


class ImagePostSeriazilizer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


# doller = cache.get_or_set('all_posts', OrderSetting.objects.first().get_doller_funtion, timeout=60*15)

def doller_funtion():
    doller = cache.get_or_set('doller', OrderSetting.objects.first().get_doller_funtion, timeout=60*15)
    return doller



class CalculatorProdcutSerialzier(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id","product_name", "price", "image", "serenaTrue_countFalse",)
    

    def get_price(self, obj):
        orders_settings = OrderSetting.objects.first()
        price = int(obj.price * orders_settings.doller)
        nds = int(orders_settings.nds * obj.price / 100 * orders_settings.doller)
        umumiy_narx = price + nds
        price = {"price": price, "nds": int(orders_settings.nds * obj.price / 100 * orders_settings.doller), "nds_narx": umumiy_narx}
        return price
    
    def get_image(self, obj):
        image = obj.image
        if image:
            return site_name + image
        return None
    


        


def kredit_cal(price, oy, foiz):
        summa = price* doller_funtion()
        data = (summa *(30.42)*foiz)/(365*100)
        return  data+(summa/oy)

class ProductSerialzier(serializers.ModelSerializer):
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField()
    kredit_summa = serializers.SerializerMethodField()
    product_video = serializers.SerializerMethodField(required=False, read_only=True)
    cashback_value = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = (  
            "id",
            "articul",
            "product_name",
            'category_name',
            "main_category",
            "super_category",
            "sub_category",
            "images",
            "product_video",
            "slug",
            "price",
            "discount_price",
            "kredit_summa",
            "short_content",
            "content",
            "tavar_dagavornaya",
            "counts",
            "articul",
            "material_nomer",
            "serenaTrue_countFalse",
            "tavar_dagavornaya",
            "counts",
            "short_description",
            "full_description",
            "cashback_value",
            )
        

    def get_cashback_value(self, obj):
        cash = cashback_values(products=[{"id": obj.id, "count": 1}])
        return int(cash["data"])
    
        
    def get_kredit_summa(self, obj):
        if obj.price:
            return int(kredit_cal(obj.price, 12, 36)) if obj.price  else 0
        return None
        

    def get_product_video(self, obj):
        if obj.product_video:
            return site_name + obj.product_video.url
        return None

    def get_price(self, obj):
        return obj.price and int(obj.price * doller_funtion()) or 0
    def get_discount_price(self, obj):
        return obj.discount_price and int(obj.discount_price * doller_funtion()) or int((obj.price * doller_funtion()) * 1.2) 
      

    
    def get_category_name(self, obj):
        if obj.super_category is not None:
            return obj.super_category.super_name 



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
            "short_description",
            "full_description",
            "discount_price",
            "short_content",
            "tavar_dagavornaya",
            "counts",
        )

    def get_price(self, obj):
        return obj.price and int(obj.price * doller_funtion()) or obj.price

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
    image = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField(read_only=True)
    kredit_summa = serializers.SerializerMethodField(read_only=True)
    cashback_value = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "category_name",
            "image",
            "product_video",
            "slug",
            "short_description",
            "price",
            "discount_price",
            "kredit_summa",
            "short_content",
            "tavar_dagavornaya",
            "counts",
            "super_category",
            "cashback_value",
            "aksiya",
        )


    def get_cashback_value(self, obj):
        cash = cashback_values(products=[{"id": obj.id, "count": 1}])
        return int(cash["data"])


    def get_kredit_summa(self, obj):
        if obj.price:
            return int(kredit_cal(obj.price, 12, 36)) if obj.price  else 0
        return None
    

    def get_discount_price(self, obj):
        if obj.price:
            return obj.discount_price and int(obj.discount_price * doller_funtion()* 1.4) or int((obj.price * doller_funtion()) * 1.3)
        

    def get_price(self, obj):
        return obj.price and int(obj.price * doller_funtion()) or 0

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
    types = serializers.CharField()
    slug = serializers.CharField()
