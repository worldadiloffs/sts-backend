from django.urls import path 
from .views import CategoryListJsonViews, CategoryHeaderViews
app_name = 'category'

urlpatterns = [
    path('<str:site>/category/category-list/', CategoryListJsonViews.as_view(), name='category-list'),
    path('<str:site>/category/header/', CategoryHeaderViews.as_view()),

]
