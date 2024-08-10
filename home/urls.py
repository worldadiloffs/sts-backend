from django.urls import path
from .views import BannerView , HomePageCategoryView , BannerDetailViews

app_name = 'home'

urlpatterns = [
    path('sts/home/banner/', BannerView.as_view()),
    path('sts/home/banner/<int:pk>/', BannerDetailViews.as_view()),
    path('sts/home/home-product/', HomePageCategoryView.as_view()),
]
