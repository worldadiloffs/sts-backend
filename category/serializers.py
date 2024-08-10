from .models import SuperCategory , MainCategory , SubCategory

from rest_framework import serializers
from config.settings import site_name


class SuperCategoryOneSeriazleir(serializers.ModelSerializer):
    category_image = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SuperCategory
        fields = "__all__"

    def get_category_image(self, obj):
        category_image = obj.category_image
        if category_image is not None:
            return site_name + category_image.url
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon is not None:
            return site_name + icon.url 
        

        
    

class SubCategoryStsSerialzier(serializers.ModelSerializer):
    sub_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = "__all__"
    def get_sub_image(self, obj):
        sub_image = obj.sub_image
        if sub_image is not None:
            return site_name + sub_image.url
        



class MainCategortStsSerializer(serializers.ModelSerializer):
    children = SubCategoryStsSerialzier(many=True, source='subcategory_set')
    main_image = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MainCategory
        fields = "__all__"

    def get_category_image(self, obj):
        category_image = obj.main_image
        if category_image is not None:
            return site_name + category_image.url
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon is not None:
            return site_name + icon.url 
        
    


class SuperCategoryStsSerializer(serializers.ModelSerializer):
    children = MainCategortStsSerializer(many=True, source='maincategory_set')
    category_image = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = SuperCategory
        fields = "__all__"
        
    def get_category_image(self, obj):
        category_image = obj.category_image
        if category_image is not None:
            return site_name + category_image.url
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon is not None:
            return site_name + icon.url 



class SubCategoryStsMiniSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", 'sub_name', 'slug', 'sub_image', 'mainCategory')


class MainCategortStsMiniSerializer(serializers.ModelSerializer):
    children = SubCategoryStsMiniSerialzier(many=True, source='subcategory_set')
    class Meta:
        model = MainCategory
        fields = ('id', 'slug', 'main_name', 'main_image', 'superCategory', 'children')


class SuperCategoryStsMiniSerializer(serializers.ModelSerializer):
    children = MainCategortStsMiniSerializer(many=True, source='maincategory_set')
    category_image = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = SuperCategory
        fields = ('id', 'slug', 'super_name', 'category_image','children')

    def get_category_image(self, obj):
        category_image = obj.category_image
        if category_image is not None:
            return site_name + category_image.url
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon is not None:
            return site_name + icon.url 


class MainCategortStsMiniHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ('id', 'slug', 'main_name', 'main_image', 'superCategory',)



class CategorySchemaserialzeir(serializers.Serializer):
    data = SuperCategoryStsMiniSerializer()
    errors = serializers.BooleanField()
    message = serializers.CharField()

class FilterCategortSchemae(serializers.Serializer):
    header_category = MainCategortStsMiniHomeSerializer()
    ommabob_category = MainCategortStsMiniHomeSerializer()



class CategoryHeaderSechema(serializers.Serializer):
    data = FilterCategortSchemae()
    errors = serializers.BooleanField()
    message = serializers.CharField()

