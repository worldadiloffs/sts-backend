from rest_framework import serializers
from .models import (Shaharlar, SiteSettings , CardGril ,  PageContent , 
                     SitePage , PaymentMethod , SocialNetwork , DeliveryService, TolovUsullar, Tumanlar, Dokon )

from config.settings import site_name

class DeliveryServiceSeriazleir(serializers.ModelSerializer):
    class Meta:
        model = DeliveryService
        fields = "__all__"

class SocialNetworkSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = "__all__"


class PaymentSerialzier(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = PaymentMethod
        fields = "__all__"

    def get_logo(self, obj):
        logo = obj.logo
        if logo:
            return site_name + logo.url
        return None

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
    icon = serializers.SerializerMethodField()
    class Meta:
        model = TolovUsullar
        fields = "__all__"

    def get_icon(self, obj):
        icon = obj.icon
        if icon:
            return site_name + icon.url
        return None

class TumanlarSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Tumanlar
        fields = "__all__"

class ShaharlarSerialzier(serializers.ModelSerializer):
    children = TumanlarSerialzier(many=True, source='tumanlar_set')
    class Meta:
        model = Shaharlar
        fields = "__all__"

class DokonSerialzier(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Dokon
        fields = "__all__"

    def get_image(self, obj):
        image = obj.image
        if image:
            return site_name + image.url
        return None




class OrderSettingsSerialzier(serializers.Serializer):
    delivery = DeliveryServiceSeriazleir(many=True, read_only=True)
    payment = TolovUsullarSerialzier(many=True, read_only=True)
    shaharlar = ShaharlarSerialzier(many=True, read_only=True)
    punkit = DokonSerialzier(many=True, read_only=True)













