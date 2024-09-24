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
    cards = AboutServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = AboutServis
        fields = ("title", "get_bground_image")


class PriceServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceServisCard
        fields = ("product_name", "count",)



class PriceServisSerializer(serializers.ModelSerializer):
    priceserviscards = PriceServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = PriceServis
        fields =("title", "price", "discount_price", "get_bground_image", "priceserviscards",)




class UstanofkaServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UstanofkaServisCard
        fields = "__all__"


class UstanofkaServisSerializer(serializers.ModelSerializer):
    cards = UstanofkaServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = UstanofkaServis
        fields = ("title", "description", "get_bground_image",)


class KomandaServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = KomandaServisCard
        fields = ("ism", "position", "get_image", "yil",)




class KomandaServisSerializer(serializers.ModelSerializer):
    cards = KomandaServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = KomandaServis
        fields = ("title", "description", "get_bground_image", )


class CategoryServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryServisCard
        fields = ("title", "text", "get_image",)


class CategoryServisSerializer(serializers.ModelSerializer):
    cards = CategoryServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = CategoryServis
        fields = ("title", "get_image", "link")


class KontaktServisSerializer(serializers.ModelSerializer):
    class Meta:
        model = KontaktServis
        fields = "__all__"

class LisenceServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LisenceServisCard
        fields = ("title", "get_imaga",)


class LisenceServisSerializer(serializers.ModelSerializer):
    cards = LisenceServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = LisenceServis
        fields = ("title", "description", "get_bground_image",)
