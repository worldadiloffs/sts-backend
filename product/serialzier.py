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
    images = ImageSeriazilizer(required=False, read_only=True, many=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ("id", "product_name", 'image', "product_picture", "product_video", "slug", "price", "discount_price", "short_content","tavar_dagavornaya","articul" , "images", "image_count", "counts")


    def get_image(self, obj):
        host = self.context.get("request")
        image = obj.image
        # print(host)
        # host_name = host

        # is_secure = "https://" if host.is_secure() else "http://"

        if image:
            return site_name  + image
        return None


class ParemententCategorySerialzeir(serializers.Serializer):
    super_id = serializers.IntegerField(required=False)
    main_id =  serializers.IntegerField(required=False)
    sub_id = serializers.IntegerField(required=False)