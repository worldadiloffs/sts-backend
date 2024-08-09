from rest_framework.views import APIView
from django.http import JsonResponse
from .models import BlogCategory , BlogHome , BlogItem , Tag
from .seralziers import BlogCategorySeriazler

class BlogListApiviews(APIView):
    def get(self, request):
        blog = BlogCategory.objects.filter(status=True, site_sts=True)
        blog_serializers = BlogCategorySeriazler(blog, many=True)
        return JsonResponse(
            {"data": blog_serializers.data, "erros": False, "message": ""}, safe=False
        )