from django.urls import path 
from .views import CategoryListJsonViews, CategoryHeaderViews
from .rtscategory import RTSCategoryListJsonViews, RTSCategoryHeaderViews

app_name = 'category'

urlpatterns = [
    path('sts/category/category-list/', CategoryListJsonViews.as_view(), name='category-list'),
    path('sts/category/header/', CategoryHeaderViews.as_view()),
    # rts site uchun categoryleri getirmek
    path('rts/category/category-list/', RTSCategoryListJsonViews.as_view(), name='category-list'),
    path('rts/category/header/', RTSCategoryHeaderViews.as_view()),
]
