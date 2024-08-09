from rest_framework import serializers
from .models import BlogCategory , Tag , BlogItem , BlogHome


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class BlogItemsSeriazler(serializers.ModelSerializer):
    tag = TagSerializers(many=True)
    class Meta:
        model = BlogItem
        fields = "__all__"

class BlogCategorySeriazler(serializers.ModelSerializer):
    children = BlogItemsSeriazler(many=True, source='blogitem_set')
    class Meta:
        model = BlogCategory
        fields = "__all__"




class BlogHomeSerialzer(serializers.ModelSerializer):
    class Meta:
        model = BlogHome
        fields = "__all__"
