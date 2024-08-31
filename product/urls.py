from django.urls import path 
from .views import  CategoryProductViews , ProductDetailApiview , SearchProductView , CartProductApiview 
from .productPost import ProductPost , ProductUpdateAPiview

app_name = "product"

urlpatterns = [
    path('<str:site>/category/<str:types>/<str:slug>/', CategoryProductViews.as_view()),
    path('<str:site>/product/<str:slug>/', ProductDetailApiview.as_view(), name='product-detail'),
    path('crm-product-post/', ProductPost.as_view()),
    path('crm-product-count-update/', ProductUpdateAPiview.as_view()),
    path('<str:site>/search/', SearchProductView.as_view(), name='search-product'),
    path('<str:site>/cart-product/', CartProductApiview.as_view()),
]
