from rest_framework import serializers
from .models import Product , Image 
from config.settings import site_name
from settings.models import OrderSetting
from category.serializers import SuperCategoryStsMiniSerializer , MainCategortStsMiniSerializer , SubCategoryStsMiniSerialzier


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
    order =  OrderSetting.objects.first() 
    return order.doller * order.nds /100

class ProductSerialzier(serializers.ModelSerializer):
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    super_category = serializers.SerializerMethodField()
    main_category = MainCategortStsMiniSerializer()
    sub_category = SubCategoryStsMiniSerialzier()

    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"




    def get_price(self, obj):
        return obj.price and obj.price * doller_funtion() or 0 
    
    def get_super_category(self, obj):
        category = obj.super_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.super_name,
                "slug": category.slug
            }
        
    def get_main_category(self, obj):
        category = obj.main_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.main_name,
                "slug": category.slug
            }
    def get_sub_category(self, obj):
        category = obj.sub_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.sub_name,
                "slug": category.slug
            }


class ProductDetailSerialzeir(serializers.ModelSerializer):
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    super_category = serializers.SerializerMethodField()
    main_category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ("id", "product_name", 'main_category','super_category', 'sub_category','images', "product_video", "slug", "price", "discount_price", "short_content","tavar_dagavornaya" , "counts", )


    
    def get_price(self, obj):
        return obj.price and obj.price * doller_funtion() or obj.price  
    
    def get_super_category(self, obj):
        category = obj.super_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.super_name,
                "slug": category.slug
            }
        
    def get_main_category(self, obj):
        category = obj.main_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.main_name,
                "slug": category.slug
            }
    def get_sub_category(self, obj):
        category = obj.sub_category
        if category is not None:
            return {
                "id": category.id,
                "category_name": category.sub_name,
                "slug": category.slug
            }


class ProductListMiniSerilizers(serializers.ModelSerializer):
    # images = ImageSeriazilizer(required=False, read_only=True, many=True)
    image = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ("id", "product_name",'category_name', 'image', "product_video", "slug", "price", "discount_price", "short_content","tavar_dagavornaya" , "counts", "super_category")

    def get_price(self, obj):
        return obj.price and obj.price * doller_funtion() or 0 
    
    def get_image(self, obj):
        image = obj.image
        if image:
            return site_name  + image
        return None
    
    def get_category_name(self, obj):
        category = obj.super_category
        if category is not None:
            return category.super_name
    


class ParemententCategorySerialzeir(serializers.Serializer):
    super_id = serializers.IntegerField(required=False)
    main_id =  serializers.IntegerField(required=False)
    sub_id = serializers.IntegerField(required=False)