from django.urls import path 
from .views import CategoryListJsonViews, CategoryHeaderViews 
from .costumAdmin import get_main_categories, get_sub_categories
app_name = 'category'

urlpatterns = [
    path('<str:site>/category/category-list/', CategoryListJsonViews.as_view(), name='category-list'),
    path('<str:site>/category/header/', CategoryHeaderViews.as_view()),
    path('get-main-categories/', get_main_categories, name='get-main-categories'),
    path('get-sub-categories/', get_sub_categories, name='get-sub-categories'),

]


