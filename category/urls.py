from django.urls import path 
from .views import CategoryListJsonViews, CategoryHeaderViews, Admin_super

app_name = 'category'

urlpatterns = [
    path('sts/category/category-list/', CategoryListJsonViews.as_view(), name='category-list'),
    path('sts/category/header/', CategoryHeaderViews.as_view()),
    path('super/', Admin_super, name='super'),
]
