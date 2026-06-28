# Controls what each page shows to the user
# Each function = one page

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.core.paginator import Paginator
import json

from .models import (
    Book, Category, Genre, UserProfile,
    Review, CartItem, WishlistItem,
    Order, OrderItem, ViewHistory,
)


# ----- HELPER: check if user is admin -----
# Used to protect admin pages from regular users
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


# ----- HOMEPAGE -----
# Shows featured books and categories
def homepage(request):
    featured_books = Book.objects.filter(is_featured=True, is_active=True)[:6]
    categories = Category.objects.all()
    return render(request, 'store/homepage.html', {
        'featured_books': featured_books,
        'categories': categories,
    })


# ----- CATALOGUE -----
# Shows all books with optional category filter
def catalogue(request):
    # Start with all active books
    books = Book.objects.filter(is_active=True)
    categories = Category.objects.all()
    selected_category = None

    # Filter by category if user clicked one
    cat_slug = request.GET.get('category', '')
    if cat_slug:
        selected_category = get_object_or_404(Category, slug=cat_slug)
        books = books.filter(category=selected_category)

    # Sort books based on user selection
    sort = request.GET.get('sort', '-created_at')
    if sort in ['price', '-price', '-created_at', 'title']:
        books = books.order_by(sort)

    # Show 12 books per page
    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'store/catalogue.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'current_sort': sort,
    })


# ----- BOOK DETAIL -----
# Shows one book's full details
def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_active=True)

    # Record that this user viewed this book (for recommender)
    if request.user.is_authenticated:
        ViewHistory.objects.update_or_create(
            user=request.user,
            book=book,
        )

    # Check if user already reviewed this book
    user_review = None
    in_wishlist = False
    in_cart = False

    if request.user.is_authenticated:
        user_review = Review.objects.filter(book=book, user=request.user).first()
        in_wishlist = WishlistItem.objects.filter(user=request.user, book=book).exists()
        in_cart = CartItem.objects.filter(user=request.user, book=book).exists()

    reviews = book.reviews.all()

    return render(request, 'store/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
        'in_cart': in_cart,
    })


# ----- SEARCH -----
# Searches books by title, author, or isbn
def search(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Search by title, author, or description
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    # ----- advanced filters -----
    cat_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    condition = request.GET.get('condition', '')

    if cat_slug:
        books = books.filter(category__slug=cat_slug)
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    if condition:
        books = books.filter(condition=condition)

    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'store/search.html', {
        'query': query,
        'page_obj': page_obj,
        'categories': categories,
        'filter_cat': cat_slug,
        'filter_min': min_price,
        'filter_max': max_price,
        'filter_condition': condition,
    })


# ----- REGISTER -----
# New user registration page
def register(request):
    # If already logged in send to homepage
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # ----- validation -----
        if not username or not email or not password1:
            messages.error(request, 'Please fill in all required fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            # Create empty profile for this user
            UserProfile.objects.create(user=user)
            # Log in automatically after registering
            login(request, user)
            messages.success(request, f'Welcome to The Book Merchant, {first_name}!')
            return redirect('homepage')

    return render(request, 'registration/register.html')


# ----- LOGIN -----
def user_login(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        # Django checks username and password against database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            # Go to page user was trying to visit before login
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


# ----- LOGOUT -----
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('homepage')


# ----- DASHBOARD -----
# Personal page showing user activity
# login_required sends non-logged-in users to /login/
@login_required
def dashboard(request):
    # Get last 6 books the user viewed
    recent_views = ViewHistory.objects.filter(user=request.user)[:6]
    # Get user wishlist
    wishlist = WishlistItem.objects.filter(user=request.user)[:4]
    # Get user orders
    orders = Order.objects.filter(user=request.user)[:5]

    return render(request, 'store/dashboard.html', {
        'recent_views': recent_views,
        'wishlist': wishlist,
        'orders': orders,
    })


# ----- PROFILE -----
# View and edit user profile info
@login_required
def profile(request):
    # Get or create profile for this user
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()

        # Update profile fields
        profile_obj.phone = request.POST.get('phone', '').strip()
        profile_obj.address = request.POST.get('address', '').strip()
        profile_obj.city = request.POST.get('city', '').strip()
        profile_obj.country = request.POST.get('country', '').strip()
        profile_obj.bio = request.POST.get('bio', '').strip()

        # Handle avatar upload
        if request.FILES.get('avatar'):
            profile_obj.avatar = request.FILES['avatar']

        profile_obj.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'store/profile.html', {
        'profile': profile_obj,
    })


# ----- CART -----
# Shows all items in the users cart
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('book')
    # Calculate total price
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


# ----- ADD TO CART -----
# AJAX: adds a book to the cart
@login_required
@require_POST
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    # Get existing cart item or create new one
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )
    if not created:
        # Book already in cart - just increase quantity
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    # Count total items in cart for the badge
    cart_count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'message': f'{book.title} added to cart!',
    })


# ----- REMOVE FROM CART -----
# AJAX: removes one item from cart
@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    cart_item.delete()
    cart_count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({'success': True, 'cart_count': cart_count})


# ----- CHECKOUT -----
# Converts cart into an order (simulated - no real payment)
@login_required
@require_POST
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    # Calculate total
    total = sum(item.subtotal for item in cart_items)

    # Create the order
    order = Order.objects.create(
        user=request.user,
        total_price=total,
    )

    # Create one order item per cart item
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            unit_price=item.book.price,
        )
        # Reduce stock
        item.book.stock = max(0, item.book.stock - item.quantity)
        item.book.save()

    # Clear the cart after order placed
    cart_items.delete()
    messages.success(request, f'Order placed successfully! Order number: {order.pk}')
    return redirect('dashboard')


# ----- WISHLIST -----
@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('book')
    return render(request, 'store/wishlist.html', {'items': items})


# ----- TOGGLE WISHLIST -----
# AJAX: adds or removes a book from wishlist
@login_required
@require_POST
def toggle_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        book=book
    )
    if not created:
        # Already in wishlist so remove it
        item.delete()
    return JsonResponse({'success': True, 'added': created})


# ----- SUBMIT REVIEW -----
# AJAX: saves a star rating and review text
@login_required
@require_POST
def submit_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    data = json.loads(request.body)
    rating = int(data.get('rating', 0))

    if not 1 <= rating <= 5:
        return JsonResponse({'success': False, 'error': 'Rating must be 1-5.'})

    # Create or update the review
    review, created = Review.objects.update_or_create(
        book=book,
        user=request.user,
        defaults={
            'rating': rating,
            'title': data.get('title', '').strip()[:150],
            'body': data.get('body', '').strip()[:2000],
        }
    )
    return JsonResponse({'success': True, 'created': created})


# ----- RECOMMENDER -----
# AJAX: returns similar books based on category and genre
def get_recommendations(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Find books in same genre first
    recs = Book.objects.filter(
        is_active=True,
        genre=book.genre
    ).exclude(pk=book.pk)[:4]

    # If not enough fill with same category books
    if recs.count() < 4:
        extra = Book.objects.filter(
            is_active=True,
            category=book.category
        ).exclude(pk=book.pk).exclude(pk__in=recs.values('pk'))[:4 - recs.count()]
        recs = list(recs) + list(extra)

    # Build JSON response
    data = [{
        'id': b.pk,
        'title': b.title,
        'author': b.author,
        'price': str(b.price),
        'cover': b.cover_image.url if b.cover_image else '',
        'url': f'/book/{b.slug}/',
    } for b in recs]

    return JsonResponse({'recommendations': data})


# ----- ADMIN DASHBOARD -----
# Only accessible by staff/superusers
@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html', {
        'book_count': Book.objects.count(),
        'user_count': User.objects.count(),
        'order_count': Order.objects.count(),
        'category_count': Category.objects.count(),
        'recent_books': Book.objects.order_by('-created_at')[:5],
        'recent_orders': Order.objects.order_by('-created_at')[:5],
    })


# ----- ADMIN BOOKS -----
@user_passes_test(is_admin, login_url='/login/')
def admin_books(request):
    books = Book.objects.all()
    return render(request, 'admin_panel/books.html', {'books': books})


# ----- ADMIN ADD BOOK -----
@user_passes_test(is_admin, login_url='/login/')
def admin_book_add(request):
    categories = Category.objects.all()
    genres = Genre.objects.all()

    if request.method == 'POST':
        # Get all form fields
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        price = request.POST.get('price', 0)
        stock = request.POST.get('stock', 0)
        category_id = request.POST.get('category')
        genre_id = request.POST.get('genre')
        description = request.POST.get('description', '').strip()
        isbn = request.POST.get('isbn', '').strip()
        condition = request.POST.get('condition', 'new')
        is_featured = request.POST.get('is_featured') == 'on'

        # Auto generate slug from title
        slug = slugify(title)

        # Create the book
        book = Book.objects.create(
            title=title,
            slug=slug,
            author=author,
            price=price,
            stock=stock,
            category_id=category_id,
            genre_id=genre_id if genre_id else None,
            description=description,
            isbn=isbn,
            condition=condition,
            is_featured=is_featured,
        )

        # Save cover image if uploaded
        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES['cover_image']
            book.save()

        messages.success(request, f'Book "{title}" added successfully!')
        return redirect('admin_books')

    return render(request, 'admin_panel/book_form.html', {
        'categories': categories,
        'genres': genres,
        'action': 'Add',
    })


# ----- ADMIN EDIT BOOK -----
@user_passes_test(is_admin, login_url='/login/')
def admin_book_edit(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    categories = Category.objects.all()
    genres = Genre.objects.all()

    if request.method == 'POST':
        book.title = request.POST.get('title', '').strip()
        book.author = request.POST.get('author', '').strip()
        book.price = request.POST.get('price', 0)
        book.stock = request.POST.get('stock', 0)
        book.category_id = request.POST.get('category')
        book.description = request.POST.get('description', '').strip()
        book.isbn = request.POST.get('isbn', '').strip()
        book.condition = request.POST.get('condition', 'new')
        book.is_featured = request.POST.get('is_featured') == 'on'

        genre_id = request.POST.get('genre')
        book.genre_id = genre_id if genre_id else None

        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES['cover_image']

        book.save()
        messages.success(request, f'Book "{book.title}" updated!')
        return redirect('admin_books')

    return render(request, 'admin_panel/book_form.html', {
        'book': book,
        'categories': categories,
        'genres': genres,
        'action': 'Edit',
    })


# ----- ADMIN DELETE BOOK -----
@user_passes_test(is_admin, login_url='/login/')
@require_POST
def admin_book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    title = book.title
    book.delete()
    messages.success(request, f'Book "{title}" deleted.')
    return redirect('admin_books')


# ----- ADMIN CATEGORIES -----
@user_passes_test(is_admin, login_url='/login/')
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/categories.html', {
        'categories': categories,
    })


# ----- ADMIN USERS -----
@user_passes_test(is_admin, login_url='/login/')
def admin_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/users.html', {'users': users})