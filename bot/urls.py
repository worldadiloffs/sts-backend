# urls.py
from django.urls import path
from . import views
app_name = 'bot'

urlpatterns = [
    path('api/attendance/', views.attendance, name='attendance'),
]
