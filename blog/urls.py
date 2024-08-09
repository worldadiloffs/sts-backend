from django.urls import path
from .views import BlogListApiviews


app_name = 'blog'

urlpatterns = [
    path('sts/blog/blog-list/', BlogListApiviews.as_view()),
]
