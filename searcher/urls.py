from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('integrate/', views.integrate, name='integrate'),
]