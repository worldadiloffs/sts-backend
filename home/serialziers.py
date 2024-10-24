from .models import   HomePageCategory , Banner , CardImage
from rest_framework import serializers 
from product.serialzier import ProductListMiniSerilizers
from config.settings import site_name
from product.servisses import get_image_url_from_cloudflare



class CardImageSerialziers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = CardImage
        fields = "__all__"

    def get_images(self, obj):
        if obj.cloudflare_id:
            return get_image_url_from_cloudflare(obj.cloudflare_id)
        image = obj.images
        if image:
            return site_name + image.url 

    

class BannerSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Banner
        fields = ( 'id', 'title', 'slug', 'status',  'category', 'image', 'cloudflare_id',)


    def get_image(self, obj):
        if obj.cloudflare_id:
            return get_image_url_from_cloudflare(obj.cloudflare_id)  # Cloudflare id bilan rasmni o'qish
        image = obj.image
        if image:
            return site_name + image.url 


class HomePageCategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = HomePageCategory
        fields = "__all__"




class ParementrHome(serializers.Serializer):
    name = serializers.CharField(required=False)


class HOmeSchemaSerialziers(serializers.Serializer):
    category_name = serializers.CharField()
    banner_image = serializers.ImageField()
    banner_image_url = serializers.URLField()
    product =  ProductListMiniSerilizers()

class ResponseHOme(serializers.Serializer):
    data = HOmeSchemaSerialziers()
    errors = serializers.BooleanField()
    message =  serializers.CharField()