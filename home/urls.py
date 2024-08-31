from django.urls import path
from .views import BannerView , HomePageCategoryView , BannerDetailViews
app_name = 'home'

urlpatterns = [
    path('<str:site>/home/banner/', BannerView.as_view()),
    path('<str:site>/home/banner/<int:pk>/', BannerDetailViews.as_view()),
    path('<str:site>/home/home-product/', HomePageCategoryView.as_view()),

]
