from django.urls import path
from . import views


urlpatterns = [
    path('test-amazon/', views.amazon, name='amazon'),
    path('test-aliexpress/', views.alik, name='alik'),
]
