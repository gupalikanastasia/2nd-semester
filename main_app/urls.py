from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('somerset/', views.somerset, name='somerset'),
    path('dcip/', views.dcip, name='dcip'),
    path('coffee/', views.bean_water, name='bean_water'),
]