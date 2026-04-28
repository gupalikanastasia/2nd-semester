from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:cat_id>/', views.category_items, name='category_page'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]