from django.urls import path
from .views import ProductSearchCalculatorView

app_name = 'calculator'

urlpatterns = [
    path('<str:site>/calculator/search', ProductSearchCalculatorView.as_view(), name='product_search_calculator_search') 
]
