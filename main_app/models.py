from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва страви")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва закладу")
    address = models.CharField(max_length=255, verbose_name="Адреса")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
