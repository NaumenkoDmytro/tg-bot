from django.urls import path
from . import views


urlpatterns = [
    path('zalupa_ebamaia/', views.index, name='index'),
]
