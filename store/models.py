# store/models.py
# This file defines all the database tables for the bookstore.
# Each class = one table in the database.

from django.db import models
from django.contrib.auth.models import User


# ----- CATEGORY TABLE -----
# Top level grouping e.g. "Fiction", "Non-Fiction"
class Category(models.Model):
    # Name of the category e.g. "Fiction"
    name = models.CharField(max_length=100)
    # Slug is the url-friendly version e.g. "fiction"
    slug = models.SlugField(max_length=100, unique=True)
    # Optional description of the category
    description = models.TextField(blank=True)

    class Meta:
        # How to display the name in Django admin
        verbose_name_plural = 'Categories'
        # Always return categories in alphabetical order
        ordering = ['name']

    def __str__(self):
        # What shows up in the admin panel for each category
        return self.name


# ----- GENRE TABLE -----
# Sub-category inside a category e.g. "Mystery" inside "Fiction"
class Genre(models.Model):
    # Each genre belongs to one category
    # if category is deleted, genres are deleted too (CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='genres'  # lets us do category.genres.all()
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.category.name} - {self.name}'


# ----- BOOK TABLE -----
# The main item in our bookstore
class Book(models.Model):

    # Book condition choices
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used - Good'),
        ('rare', 'Rare / Collectors'),
    ]

    # ----- relationships -----
    # Each book belongs to one category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # if category deleted, book stays but category is null
        null=True,
        related_name='books'  # lets us do category.books.all()
    )
    # Each book belongs to one genre (optional)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    # ----- book details -----
    title = models.CharField(max_length=255)
    # Slug is the url-friendly version e.g. "the-great-gatsby"
    slug = models.SlugField(max_length=255, unique=True)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    # ISBN is the unique book number
    isbn = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    published_year = models.PositiveIntegerField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)

    # ----- pricing and stock -----
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new'
    )

    # ----- image -----
    # Book cover image - stored in media/book_covers/
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )

    # ----- flags -----
    # Featured books show on the homepage
    is_featured = models.BooleanField(default=False)
    # Inactive books are hidden from customers
    is_active = models.BooleanField(default=True)

    # ----- timestamps -----
    # Set automatically when book is created
    created_at = models.DateTimeField(auto_now_add=True)
    # Updated automatically every time book is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Newest books first
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} by {self.author}'

    # Check if book is in stock
    @property
    def in_stock(self):
        return self.stock > 0
    # calculate average star rating from all reviews
    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    # count total number of reviews
    @property
    def review_count(self):
        return self.reviews.count()
    
    


# ----- USER PROFILE TABLE -----
# Extra info for each user beyond what Django stores by default
class UserProfile(models.Model):
    # One profile per user - if user deleted, profile deleted too
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # Optional extra fields
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    # Profile picture stored in media/avatars/
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    # Short bio about the user
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


# ----- REVIEW TABLE -----
# A star rating and text review left by a logged in user
class Review(models.Model):
    # Each review belongs to one book and one user
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'  # lets us do book.reviews.all()
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    # Rating must be 1 to 5 stars
    rating = models.PositiveSmallIntegerField()
    # Optional review title and body text
    title = models.CharField(max_length=150, blank=True)
    body = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One review per user per book - no duplicates
        unique_together = ('book', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} rated {self.book.title} - {self.rating} stars'


# ----- CART ITEM TABLE -----
# One row per book in the users shopping basket
class CartItem(models.Model):
    # Cart item belongs to one user and one book
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    # How many copies of this book in cart
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One row per book per user (quantity increases instead of new rows)
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.username} - {self.book.title} x{self.quantity}'

    # Calculate total price for this cart item
    @property
    def subtotal(self):
        return self.book.price * self.quantity


# ----- WISHLIST ITEM TABLE -----
# Books the user has saved for later
class WishlistItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One row per book per user
        unique_together = ('user', 'book')
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user.username} wishlist - {self.book.title}'


# ----- ORDER TABLE -----
# A completed purchase by a user
class Order(models.Model):

    # Order status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    # Total price is saved at time of purchase
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.pk} by {self.user.username}'


# ----- ORDER ITEM TABLE -----
# One row per book inside an order
class OrderItem(models.Model):
    # Each order item belongs to one order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    # Save the price at time of purchase in case price changes later
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.book.title} x{self.quantity} in Order {self.order.pk}'

    # Total price for this order item
    @property
    def subtotal(self):
        return self.unit_price * self.quantity


# ----- VIEW HISTORY TABLE -----
# Tracks which books each user has viewed
# Used by the recommender system to suggest similar books
class ViewHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='view_history'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='view_history'
    )
    # auto_now updates the time every time user views the book again
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        # One row per user per book
        unique_together = ('user', 'book')
        ordering = ['-viewed_at']

    def __str__(self):
        return f'{self.user.username} viewed {self.book.title}'