from rest_framework import serializers
from .models import (Shaharlar, SiteSettings , CardGril ,  PageContent , 
                     SitePage , PaymentMethod , SocialNetwork , DeliveryService, TolovUsullar, Tumanlar, Dokon )


class DeliveryServiceSeriazleir(serializers.ModelSerializer):
    class Meta:
        model = DeliveryService
        fields = "__all__"

class SocialNetworkSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = "__all__"


class PaymentSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"

class SettingsSeriazlier(serializers.ModelSerializer):
    socialnetwork = SocialNetworkSerialzier(many=True, read_only=True)
    class Meta:
        model = SiteSettings
        fields=  "__all__"


class CardGrilSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CardGril
        fields = "__all__"

class PageContentSerialzier(serializers.ModelSerializer):
    card = CardGrilSerialzer(many=True, read_only=True)
    class Meta:
        model = PageContent
        fields = "__all__"



class SitePageSerialzier(serializers.ModelSerializer):
    children = PageContentSerialzier(many=True, source='pagecontent_set')
    class Meta:
        model = SitePage
        fields = "__all__"


class TolovUsullarSerialzier(serializers.ModelSerializer):
    payment_methods = PaymentSerialzier(many=True)
    class Meta:
        model = TolovUsullar
        fields = "__all__"

class TumanlarSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Tumanlar
        fields = "__all__"

class ShaharlarSerialzier(serializers.ModelSerializer):
    viloyat = TumanlarSerialzier(many=True)
    class Meta:
        model = Shaharlar
        fields = "__all__"

class DokonSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Dokon
        fields = "__all__"




class OrderSettingsSerialzier(serializers.Serializer):
    delivery = DeliveryServiceSeriazleir(many=True, read_only=True)
    payment = TolovUsullarSerialzier(many=True, read_only=True)
    shaharlar = ShaharlarSerialzier(many=True, read_only=True)
    punkit = DokonSerialzier(many=True, read_only=True)









