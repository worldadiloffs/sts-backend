from rest_framework import serializers
from .models import Product , Image 
from config.settings import site_name


class ImageSeriazilizer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"




class ProductSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerialzeir(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductListMiniSerilizers(serializers.ModelSerializer):
    # images = ImageSeriazilizer(required=False, read_only=True, many=True)
    image = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ("id", "product_name", 'image', "product_video", "slug", "price", "discount_price", "short_content","tavar_dagavornaya" , "counts", "super_category")


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