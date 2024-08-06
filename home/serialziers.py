from .models import homePage , HomePageCategory , Banner
from rest_framework import serializers 

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class HomePageSerializers(serializers.ModelSerializer):
    class Meta:
        model = homePage
        fields = "__all__"



class HomePageCategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = HomePageCategory
        fields = "__all__"




