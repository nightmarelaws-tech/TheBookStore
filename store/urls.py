from django.urls import path
from . import views

urlpatterns = [
    # ----- public pages -----
    path('', views.homepage, name='homepage'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),

    # ----- search -----
    path('search/', views.search, name='search'),

    # ----- auth -----
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ----- user account -----
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # ----- cart -----
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

    # ----- wishlist -----
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # ----- reviews -----
    path('review/<int:book_id>/submit/', views.submit_review, name='submit_review'),

    # ----- recommender -----
    path('api/recommendations/<int:book_id>/', views.get_recommendations, name='recommendations'),

    # ----- admin panel -----
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/books/', views.admin_books, name='admin_books'),
    path('admin-panel/books/add/', views.admin_book_add, name='admin_book_add'),
    path('admin-panel/books/<int:book_id>/edit/', views.admin_book_edit, name='admin_book_edit'),
    path('admin-panel/books/<int:book_id>/delete/', views.admin_book_delete, name='admin_book_delete'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
]