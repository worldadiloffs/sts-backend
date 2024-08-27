from rest_framework.views import APIView
from django.http import JsonResponse
from .models import BlogCategory , BlogHome , BlogItem , Tag
from .seralziers import BlogCategorySeriazler , TagSerializers
from rest_framework import serializers , status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from rest_framework.generics import ListAPIView, RetrieveAPIView
class BlogSchemaSerialzier(serializers.Serializer):
    data = BlogCategorySeriazler()
    errors = serializers.BooleanField()
    message = serializers.CharField()


class BlogListApiviews(APIView):
    @extend_schema(
            responses=BlogSchemaSerialzier()
    )
    def get(self, request):
        blog = BlogCategory.objects.filter(status=True, site_sts=True)
        blog_serializers = BlogCategorySeriazler(blog, many=True)
        return JsonResponse(
            {"data": blog_serializers.data, "erros": False, "message": ""}, safe=False
        )
    



class TagApiviews(ListAPIView):
    def get(self, request):
        expected_data = {"data":"success", "errors": False, "message": ""},
        return Response(data=expected_data, status=200)