from django.urls import path 
from .views import ProductListMiniView , CategoryProductViews 
from .productPost import ProductPostApiView

app_name = "product"

urlpatterns = [
    path('sts/product/product-listt/', ProductListMiniView.as_view(), name='product-list'),
    path('sts/product/category-product/', CategoryProductViews.as_view()),
    path('prod-post/', ProductPostApiView.as_view()),
]
