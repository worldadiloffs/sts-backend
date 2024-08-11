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
        if category_image:
            return site_name + category_image.url
        return None
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon:
            return site_name + icon.url 
        return None
        

        
    

class SubCategoryStsSerialzier(serializers.ModelSerializer):
    sub_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = "__all__"
    def get_sub_image(self, obj):
        sub_image = obj.sub_image
        if sub_image:
            return site_name + sub_image.url
        return None
        



class MainCategortStsSerializer(serializers.ModelSerializer):
    children = SubCategoryStsSerialzier(many=True, source='subcategory_set')
    main_image = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MainCategory
        fields = "__all__"

    def get_main_image(self, obj):
        category_image = obj.main_image
        if category_image:
            return site_name + category_image.url
        return None
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon:
            return site_name + icon.url 
        return None
        
    


class SuperCategoryStsSerializer(serializers.ModelSerializer):
    children = MainCategortStsSerializer(many=True, source='maincategory_set')
    category_image = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = SuperCategory
        fields = "__all__"

    def get_category_image(self, obj):
        category_image = obj.category_image
        if category_image:
            return site_name + category_image.url
        return None
        
    def get_icon(self, obj):
        icon = obj.icon
        if icon:
            return site_name + icon.url 
        return None



class SubCategoryStsMiniSerialzier(serializers.ModelSerializer):
    sub_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = ("id", 'sub_name', 'slug', 'sub_image', 'mainCategory')

    def get_sub_image(self, obj):
        sub_image = obj.sub_image
        if sub_image:
            return site_name + sub_image.url



class MainCategortStsMiniSerializer(serializers.ModelSerializer):
    children = SubCategoryStsMiniSerialzier(many=True, source='subcategory_set')
    main_image = serializers.SerializerMethodField(read_only=True)
    main_icon = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MainCategory
        fields = ('id', 'slug', 'main_name', 'main_image', 'main_icon','superCategory', 'children')

    
    def get_main_image(self, obj):
        category_image = obj.main_image
        if category_image:
            return site_name + category_image.url
        return None
        
    def get_main_icon(self, obj):
        icon = obj.icon
        if icon:
            return site_name + icon.url 
        return None


class SuperCategoryStsMiniSerializer(serializers.ModelSerializer):
    children = MainCategortStsMiniSerializer(many=True, source='maincategory_set')
    images = serializers.SerializerMethodField()
    super_icon = serializers.SerializerMethodField()
    class Meta:
        model  = SuperCategory
        fields = ('id', 'slug', 'super_name','images', 'super_icon',  'category_image','children')

    def get_images(self, obj):
        category_image = obj.category_image
        if category_image :
            return site_name + category_image.url
        return None
        
    def get_super_icon(self, obj):
        icon = obj.icon
        if icon:
            return site_name + icon.url 
        return None


class MainCategortStsMiniHomeSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MainCategory
        fields = ('id', 'slug', 'main_name', 'main_image', 'superCategory',)
    
    def get_main_image(self, obj):
        image = obj.main_image
        if image:
            return site_name + image.url
        return None







# Schema serialziers 

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

