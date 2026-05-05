from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .forms import SubscriptionForm, RatingForm, GuestOrderForm, PandyRegisterForm
from .models import Category, MenuItem, Order, OrderItem, Rating, Subscription


# ──────────────────────────────────────────────
# Головна / категорії
# ──────────────────────────────────────────────

def home(request):
    subscription_form = SubscriptionForm()
    subscription_message = None

    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form, subscription_message = _handle_subscription(request)

    return render(request, 'main_app/index.html', {
        'title': 'Головна: Sleepy Pandy',
        'categories': Category.objects.all(),
        'items': MenuItem.objects.all(),
        'page_type': 'home',
        'subscription_form': subscription_form,
        'subscription_message': subscription_message,
    })


def category_items(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    subscription_form = SubscriptionForm()
    subscription_message = None

    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form, subscription_message = _handle_subscription(request)

    return render(request, 'main_app/index.html', {
        'title': category.name,
        'categories': Category.objects.all(),
        'items': MenuItem.objects.filter(category=category),
        'page_type': 'category',
        'subscription_form': subscription_form,
        'subscription_message': subscription_message,
    })


# ──────────────────────────────────────────────
# Деталі товару
# ──────────────────────────────────────────────

def item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    categories = Category.objects.all()
    already_rated = False

    if request.user.is_authenticated:
        already_rated = Rating.objects.filter(item=item, user=request.user).exists()

    rating_form = RatingForm()

    if request.method == 'POST' and 'score' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        if not already_rated:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                new_rating = rating_form.save(commit=False)
                new_rating.item = item
                new_rating.user = request.user
                new_rating.save()
                return redirect('item_detail', item_id=item.id)

    return render(request, 'main_app/item_detail.html', {
        'item': item,
        'categories': categories,
        'title': item.name,
        'rating_form': rating_form,
        'already_rated': already_rated,
    })


# ──────────────────────────────────────────────
# Кошик
# ──────────────────────────────────────────────

def cart_add(request, item_id):
    cart = request.session.get('cart', {})
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1
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
        items_in_cart.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'main_app/cart.html', {
        'items': items_in_cart,
        'total_price': total_price,
        'categories': Category.objects.all(),
        'title': 'Ваш кошик',
    })


def cart_remove(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    return redirect('cart_detail')


# ──────────────────────────────────────────────
# Оформлення замовлення
# ──────────────────────────────────────────────

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    # Рахуємо загальну суму
    total_price = 0
    cart_items = []
    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        subtotal = item.price * quantity
        total_price += subtotal
        cart_items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, total_price=total_price)
            customer_email = request.user.email
            customer_name = request.user.username
        else:
            form = GuestOrderForm(request.POST)
            if not form.is_valid():
                return render(request, 'main_app/checkout.html', {
                    'form': form,
                    'total_price': total_price,
                    'categories': Category.objects.all(),
                })
            order = form.save(commit=False)
            order.total_price = total_price
            order.save()
            customer_email = form.cleaned_data.get('email', '')
            customer_name = form.cleaned_data.get('first_name', 'Гість')

        # Зберігаємо позиції замовлення
        for item_id, quantity in cart.items():
            item = get_object_or_404(MenuItem, id=item_id)
            OrderItem.objects.create(
                order=order, product=item, quantity=quantity, price=item.price
            )

        # Надсилаємо email підтвердження
        _send_order_email(order, cart_items, total_price, customer_email, customer_name)

        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)

    form = GuestOrderForm() if not request.user.is_authenticated else None
    return render(request, 'main_app/checkout.html', {
        'form': form,
        'total_price': total_price,
        'categories': Category.objects.all(),
        'title': 'Оформлення замовлення',
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main_app/order_success.html', {
        'order': order,
        'categories': Category.objects.all(),
    })


# ──────────────────────────────────────────────
# Авторизація / Профіль
# ──────────────────────────────────────────────

def register(request):
    if request.method == 'POST':
        form = PandyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PandyRegisterForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'categories': Category.objects.all(),
    })


@login_required
def profile(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'main_app/profile.html', {
        'orders': orders,
        'categories': Category.objects.all(),
    })


# ──────────────────────────────────────────────
# Допоміжні функції
# ──────────────────────────────────────────────

def _handle_subscription(request):
    """Обробляє підписку на розсилку. Повертає (форму, повідомлення)."""
    form = SubscriptionForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        if Subscription.objects.filter(email=email).exists():
            return SubscriptionForm(), '⚠️ Цей email вже підписаний на розсилку!'
        form.save()

        # Лист підтвердження підписки
        try:
            send_mail(
                subject='Ласкаво просимо до Sleepy Pandy! 🐼',
                message=(
                    f"Привіт, {form.cleaned_data['name']}!\n\n"
                    "Дякуємо, що підписалися на наші новини. "
                    "Ми будемо надсилати вам найсмачніші оновлення меню та акції ☕🍰\n\n"
                    "З любов'ю, команда Sleepy Pandy"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

        return SubscriptionForm(), '✅ Дякуємо! Ви успішно підписалися на наші новини 🐼'
    return form, None


def _send_order_email(order, cart_items, total_price, customer_email, customer_name):
    """Надсилає email з підтвердженням замовлення клієнту та адміну."""
    items_text = '\n'.join(
        f"  • {entry['item'].name} × {entry['quantity']} = {entry['subtotal']} грн"
        for entry in cart_items
    )
    message = (
        f"Привіт, {customer_name}! 🐼\n\n"
        f"Ваше замовлення №{order.id} прийнято!\n\n"
        f"Склад замовлення:\n{items_text}\n\n"
        f"Загальна сума: {total_price} грн\n\n"
        "Ми зв'яжемося з вами найближчим часом для підтвердження.\n\n"
        "З любов'ю, Sleepy Pandy ☕"
    )

    # Лист клієнту
    if customer_email:
        try:
            send_mail(
                subject=f'Замовлення №{order.id} прийнято — Sleepy Pandy 🐼',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[customer_email],
                fail_silently=True,
            )
        except Exception:
            pass

    # Лист адміну
    try:
        send_mail(
            subject=f'[Адмін] Нове замовлення №{order.id}',
            message=f"Нове замовлення від {customer_name}.\n\n{items_text}\n\nСума: {total_price} грн",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )
    except Exception:
        pass

import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

class UnsafeEmailBackend(SMTPEmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                ctx = ssl._create_unverified_context()
                self.connection.starttls(context=ctx)
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise
            return False