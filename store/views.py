# This file controls what each page shows to the user

from django.shortcuts import render
from .models import Book, Category

# ----- HOMEPAGE VIEW -----
# Shows featured books and categories on the homepage
def homepage(request):
    # Get only featured and active books for the homepage
    featured_books = Book.objects.filter(is_featured=True, is_active=True)[:6]
    # Get all categories for the category section
    categories = Category.objects.all()

    return render(request, 'store/homepage.html', {
        'featured_books': featured_books,
        'categories': categories,
    })