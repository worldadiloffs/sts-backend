from .models import homePage , HomePageCategory , Banner
from rest_framework import serializers 
from product.serialzier import ProductListMiniSerilizers
from config.settings import site_name


class BannerSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Banner
        fields = ('title', 'slug', 'status',  'category', 'image')


    def get_image(self, obj):
        image = obj.image
        if image:
            return site_name + image.url 
        

        


class HomePageSerializers(serializers.ModelSerializer):
    class Meta:
        model = homePage
        fields = "__all__"



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