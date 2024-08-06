from django.urls import path 
from .views import CategoryListJsonViews, MainCategoryViews
app_name = 'category'

urlpatterns = [
    path('sts/category/category-list/', CategoryListJsonViews.as_view(), name='category-list'),
    path('sts/category/header/', MainCategoryViews.as_view()),
]
