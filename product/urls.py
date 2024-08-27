from django.urls import path 
from .views import ProductListMiniView , CategoryProductViews , ProductDetailApiview , ImageProductApiview, SearchProductView , CartProductApiview 
from .productPost import ProductPost , ProductUpdateAPiview
from product.rtsproduct.views import RTSProductListMiniView , RTSProductDetailApiview , RTSSearchProductView , RTSCartProductApiview, RTSCategoryProductViews

app_name = "product"

urlpatterns = [
    path('sts/product/product-list/', ProductListMiniView.as_view(), name='product-list'),
    path('sts/category/<str:types>/<str:slug>/', CategoryProductViews.as_view()),
    path('sts/product/<str:slug>/', ProductDetailApiview.as_view(), name='product-detail'),
    path('crm-product-post/', ProductPost.as_view()),
    path('crm-product-count-update/', ProductUpdateAPiview.as_view()),
    path('image-product/', ImageProductApiview.as_view()),
    path('sts/search/', SearchProductView.as_view(), name='search-product'),
    path('sts/cart-product/', CartProductApiview.as_view()),
    #rts site uchun api 
    path('rts/product/product-list/', RTSProductListMiniView.as_view(), name='rts-product-list'),
    path('rts/category/<str:types>/<str:slug>/', RTSCategoryProductViews.as_view()),
    path('rts/product/<str:slug>/', RTSProductDetailApiview.as_view(), name='rts-product-detail'),
    path('rts/search/', RTSSearchProductView.as_view(), name='rts-search-product'),
    path('rts/cart-product/', RTSCartProductApiview.as_view()),
]
