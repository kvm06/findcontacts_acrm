from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('integrate/', views.integrate, name='integrate'),
    path('contacts/', views.get_contact, name='get_contact'),
]
