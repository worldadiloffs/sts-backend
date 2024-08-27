from rest_framework import serializers
from .models import BlogCategory , Tag , BlogItem , BlogHome


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("title", "id")

    def validate_title(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Title can't be a number.")
        return value

class BlogItemsSeriazler(serializers.ModelSerializer):
    tag = TagSerializers(many=True)
    class Meta:
        model = BlogItem
        fields = "__all__"

    def validate_title(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Title can't be a number.")
        return value

class BlogCategorySeriazler(serializers.ModelSerializer):
    children = BlogItemsSeriazler(many=True, source='blogitem_set')
    class Meta:
        model = BlogCategory
        fields = "__all__"




class BlogHomeSerialzer(serializers.ModelSerializer):
    class Meta:
        model = BlogHome
        fields = "__all__"
