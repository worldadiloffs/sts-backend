from rest_framework import serializers
from .models  import (JopServis, JopServisCard, AboutServis, AboutServisCard, PriceServis, 
                      PriceServisCard, UstanofkaServis, UstanofkaServisCard, KomandaServis, KomandaServisCard, CategoryServis, CategoryServisCard, KontaktServis, LisenceServis, LisenceServisCard)


class JopServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JopServisCard
        fields = ("title", "text", "get_image",)



class JopServisSerializer(serializers.ModelSerializer):
    jopserviscards = JopServisCardSerializer(required=False, read_only=True, many=True)
    class Meta:
        model = JopServis
        fields = ("header_title", "header_title_text", "get_bground_image", "status", "jopserviscards",)





class AboutServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutServisCard
        fields = ("title", "text", "get_image",)


class AboutServisSerializer(serializers.ModelSerializer):
    aboutserviscards = AboutServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = AboutServis
        fields = ("title", "get_bground_image", "aboutserviscards",)


#   content = models.TextField(max_length=500, blank=True , null=True)
#     narx = models.PositiveIntegerField(blank=True, null=True)
#     arzonlashgan_narx = models.PositiveIntegerField(blank=True, null=True)

class PriceServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceServisCard
        fields = ("product_content",'content', "narx", "arzonlashgan_narx",)



class PriceServisSerializer(serializers.ModelSerializer):
    priceserviscards = PriceServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = PriceServis
        fields =("title", "get_bground_image", "priceserviscards",)




class UstanofkaServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UstanofkaServisCard
        fields = "__all__"


class UstanofkaServisSerializer(serializers.ModelSerializer):
    ustanofkaserviscards = UstanofkaServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = UstanofkaServis
        fields = ("title", "description", "get_bground_image",'ustanofkaserviscards',)


class KomandaServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = KomandaServisCard
        fields = ("ism", "position", "get_image", "yil",)




class KomandaServisSerializer(serializers.ModelSerializer):
    komandaserviscard = KomandaServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = KomandaServis
        fields = ("title", "description", "get_bground_image", 'komandaserviscard',)


class CategoryServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryServisCard
        fields = ("title", "text", "get_image",)


class CategoryServisSerializer(serializers.ModelSerializer):
    children = CategoryServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = CategoryServis
        fields = ("title", "get_image", "link", "children",)


class KontaktServisSerializer(serializers.ModelSerializer):
    class Meta:
        model = KontaktServis
        fields = "__all__"

class LisenceServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LisenceServisCard
        fields = ("title", "get_imaga",)


class LisenceServisSerializer(serializers.ModelSerializer):
    lisenceserviscards = LisenceServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = LisenceServis
        fields = ("title", "description", "get_bground_image",'lisenceserviscards',)
