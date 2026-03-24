from django.shortcuts import render
from .models import Category, MenuItem

def home(request):
    context = {
        'title': 'Головна: Sleepy Pandy',
        'categories': Category.objects.all(),
        'items': MenuItem.objects.all(),
        'page_type': 'home'
    }
    return render(request, 'main_app/index.html', context)

def category_items(request, cat_id):
    category = Category.objects.get(id=cat_id)
    context = {
        'title': category.name,
        'categories': Category.objects.all(),
        'items': MenuItem.objects.filter(category=category),
        'page_type': 'category'
    }
    return render(request, 'main_app/index.html', context)