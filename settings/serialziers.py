from rest_framework import serializers
from .models import SiteSettings , CardGril , Page , PageContent 

class SettingsSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields=  "__all__"


class CardGrilSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CardGril
        fields = "__all__"

class PageContentSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = "__all__"


class PageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Page 
        fields = "__all__"


