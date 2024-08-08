from rest_framework import serializers
from .models import Product , Image 


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
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    class Meta:
        model = Product
        fields = ["id", "product_name", "product_picture", "product_video", "slug", "price", "discount_price", "short_content","tavar_dagavornaya","articul" , "images", "image_count"]


    # def get_image(self, obj):
    #     host = self.context.get("request")
    #     image = obj.image
    #     # host_name = host.get_host()

    #     # is_secure = "https://" if host.is_secure() else "http://"

    #     if image:
    #         return  image
    #     return None
