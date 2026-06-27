# store/admin.py
# Register our models here so we can see them in the Django admin panel

from django.contrib import admin
from .models import Category, Genre, Book, UserProfile, Review, CartItem, WishlistItem, Order, OrderItem, ViewHistory

# Register each model so it shows in /django-admin/
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ViewHistory)