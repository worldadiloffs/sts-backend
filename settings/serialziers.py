from rest_framework import serializers
from .models import SiteSettings , CardGril ,  PageContent , SitePage , PaymentMethod , SocialNetwork , DeliveryService 


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



