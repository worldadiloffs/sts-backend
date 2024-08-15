from django.urls import path 
from .views import ProductListMiniView , CategoryProductViews , ProductDetailApiview , ImageProductApiview, SearchProductView
from .productPost import ProductPost , ProductUpdateAPiview

app_name = "product"

urlpatterns = [
    path('sts/product/product-list/', ProductListMiniView.as_view(), name='product-list'),
    path('sts/category/<str:types>/<str:slug>/', CategoryProductViews.as_view()),
    path('sts/product/<str:slug>/', ProductDetailApiview.as_view(), name='product-detail'),
    path('crm-product-post/', ProductPost.as_view()),
    path('crm-product-count-update/', ProductUpdateAPiview.as_view()),
    path('image-product/', ImageProductApiview.as_view()),
    path('sts/search/', SearchProductView.as_view(), name='search-product'),

]
