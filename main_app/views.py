from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubscriptionForm, RatingForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Order

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

def item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    categories = Category.objects.all() # для меню
    return render(request, 'main_app/item_detail.html', {
        'item': item,
        'categories': categories,
        'title': item.name
    })

def item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            new_rating = rating_form.save(commit=False)
            new_rating.item = item
            new_rating.save()
            return redirect('item_detail', item_id=item.id)
    else:
        rating_form = RatingForm()

    return render(request, 'main_app/item_detail.html', {
        'item': item,
        'categories': categories,
        'title': item.name,
        'rating_form': rating_form,
        'subscription_form': SubscriptionForm()  # Передаємо форму розсилки
    })

def cart_add(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)

    if item_id_str in cart:
        cart[item_id_str] += 1
    else:
        cart[item_id_str] = 1

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    items_in_cart = []
    total_price = 0

    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        subtotal = item.price * quantity
        total_price += subtotal
        items_in_cart.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal
        })

    categories = Category.objects.all()
    return render(request, 'main_app/cart.html', {
        'items': items_in_cart,
        'total_price': total_price,
        'categories': categories,
        'title': 'Ваш кошик'
    })


def cart_remove(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        del cart[item_id_str]
        request.session['cart'] = cart
    return redirect('cart_detail')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    if request.user.is_staff:
        # Адмін бачить замовлення всіх
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Звичайний юзер бачить тільки свої
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'main_app/profile.html', {'orders': orders})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    total_price = 0
    # Спершу рахуємо загальну суму
    for item_id, quantity in cart.items():
        item = MenuItem.objects.get(id=item_id)
        total_price += item.price * quantity

    # Створюємо замовлення
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Додаємо товари в замовлення
    for item_id, quantity in cart.items():
        item = MenuItem.objects.get(id=item_id)
        OrderItem.objects.create(order=order, product=item, quantity=quantity, price=item.price)

    # Очищуємо кошик
    request.session['cart'] = {}
    return redirect('profile')