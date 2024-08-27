from django.urls import path
from .views import BlogListApiviews, TagApiviews


app_name = 'blog'

urlpatterns = [
    path('sts/blog/blog-list/', BlogListApiviews.as_view()),
    path('tag/list/', TagApiviews.as_view(), name='tag-list'),
]
