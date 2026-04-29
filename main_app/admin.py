from django.contrib import admin
from .models import Category, MenuItem, Location, Subscription, Rating, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at', 'updated_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at') # Бачимо імейли підписників
    search_fields = ('email',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('item', 'score', 'created_at')
    list_filter = ('score', 'item')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Щоб не було порожніх рядків

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    list_filter = ('created_at', 'user')
    inlines = [OrderItemInline]
