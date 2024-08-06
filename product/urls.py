from django.urls import path 
from .views import ProductListMiniView , CategoryProductViews

app_name = "product"

urlpatterns = [
    path('sts/product/product-list/', ProductListMiniView.as_view(), name='product-list'),
    path('sts/product/category-product/', CategoryProductViews.as_view()),
]
