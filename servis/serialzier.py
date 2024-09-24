from rest_framework import serializers
from .models  import (JopServis, JopServisCard, AboutServis, AboutServisCard, PriceServis, 
                      PriceServisCard, UstanofkaServis, UstanofkaServisCard, KomandaServis, KomandaServisCard, CategoryServis, CategoryServisCard, KontaktServis, LisenceServis, LisenceServisCard)


class JopServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JopServisCard
        fields = "__all__"


class JopServisSerializer(serializers.ModelSerializer):
    cards = JopServisCardSerializer( required=False , many=True, read_only=True)
    class Meta:
        model = JopServis
        fields = "__all__"



class AboutServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutServisCard
        fields = "__all__"


class AboutServisSerializer(serializers.ModelSerializer):
    cards = AboutServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = AboutServis
        fields = "__all__"


class PriceServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceServisCard
        fields = "__all__"


class PriceServisSerializer(serializers.ModelSerializer):
    cards = PriceServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = PriceServis
        fields = "__all__"

class UstanofkaServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UstanofkaServisCard
        fields = "__all__"


class UstanofkaServisSerializer(serializers.ModelSerializer):
    cards = UstanofkaServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = UstanofkaServis
        fields = "__all__"


class KomandaServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = KomandaServisCard
        fields = "__all__"

class KomandaServisSerializer(serializers.ModelSerializer):
    cards = KomandaServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = KomandaServis
        fields = "__all__"


class CategoryServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryServisCard
        fields = "__all__"


class CategoryServisSerializer(serializers.ModelSerializer):
    cards = CategoryServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = CategoryServis
        fields = "__all__"


class KontaktServisSerializer(serializers.ModelSerializer):
    class Meta:
        model = KontaktServis
        fields = "__all__"

class LisenceServisCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LisenceServisCard
        fields = "__all__"


class LisenceServisSerializer(serializers.ModelSerializer):
    cards = LisenceServisCardSerializer(required=False , many=True, read_only=True)
    class Meta:
        model = LisenceServis
        fields = "__all__"

