from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:cat_id>/', views.category_items, name='category_page'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]