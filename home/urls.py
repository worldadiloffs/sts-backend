from django.urls import path
from .views import BannerView , HomePageCategoryView , BannerDetailViews
from .rtshomeview import RTSBannerView, RTSBannerDetailViews, RTSHomePageCategoryView

app_name = 'home'

urlpatterns = [
    path('sts/home/banner/', BannerView.as_view()),
    path('sts/home/banner/<int:pk>/', BannerDetailViews.as_view()),
    path('sts/home/home-product/', HomePageCategoryView.as_view()),
    # rts site uchun home view
    path('rts/home/banner/', RTSBannerView.as_view()),
    path('rts/home/banner/<int:pk>/', RTSBannerDetailViews.as_view()),
    path('rts/home/home-product/', RTSHomePageCategoryView.as_view()),

]
