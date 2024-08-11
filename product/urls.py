from django.urls import path 
from .views import ProductListMiniView , CategoryProductViews , ProductDetailApiview
from .productPost import ProductPost

app_name = "product"

urlpatterns = [
    path('sts/product/product-list/', ProductListMiniView.as_view(), name='product-list'),
    path('sts/category/<str:types>/<str:slug>/', CategoryProductViews.as_view()),
    path('sts/product/<str:slug>/', ProductDetailApiview.as_view(), name='product-detail'),
    path('crm-product-post/', ProductPost.as_view()),

]
