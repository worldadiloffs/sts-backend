from .models import SuperCategory , MainCategory , SubCategory

from rest_framework import serializers


class SuperCategoryOneSeriazleir(serializers.ModelSerializer):
    class Meta:
        model = SuperCategory
        fields = "__all__"





class SubCategoryStsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class MainCategortStsSerializer(serializers.ModelSerializer):
    children = SubCategoryStsSerialzier(many=True, source='subcategory_set')
    class Meta:
        model = MainCategory
        fields = "__all__"


class SuperCategoryStsSerializer(serializers.ModelSerializer):
    children = MainCategortStsSerializer(many=True, source='maincategory_set')
    class Meta:
        model  = SuperCategory
        fields = "__all__"





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
    class Meta:
        model  = SuperCategory
        fields = ('id', 'slug', 'super_name', 'category_image','children')


class MainCategortStsMiniHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ('id', 'slug', 'main_name', 'main_image', 'superCategory',)


