# add_data.py
# Run this script to add categories, genres and books to the database
# Usage: python add_data.py

import os
import django

# tell Python which settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmerchant.settings')
django.setup()

from store.models import Category, Genre, Book

# ----- add categories -----
print("Adding categories...")
fiction,      _ = Category.objects.get_or_create(name='Fiction',     slug='fiction')
nonfiction,   _ = Category.objects.get_or_create(name='Non-Fiction', slug='non-fiction')
manga,        _ = Category.objects.get_or_create(name='Manga',       slug='manga')
science,      _ = Category.objects.get_or_create(name='Science',     slug='science')
children,     _ = Category.objects.get_or_create(name="Children's",  slug='children')
history,      _ = Category.objects.get_or_create(name='History',     slug='history')
biography,    _ = Category.objects.get_or_create(name='Biography',   slug='biography')
mystery_cat,  _ = Category.objects.get_or_create(name='Mystery',     slug='mystery')

# ----- add genres -----
print("Adding genres...")
fantasy,   _ = Genre.objects.get_or_create(name='Fantasy',   slug='fantasy',   category=fiction)
romance,   _ = Genre.objects.get_or_create(name='Romance',   slug='romance',   category=fiction)
mystery,   _ = Genre.objects.get_or_create(name='Mystery',   slug='mystery',   category=fiction)
thriller,  _ = Genre.objects.get_or_create(name='Thriller',  slug='thriller',  category=fiction)
shonen,    _ = Genre.objects.get_or_create(name='Shonen',    slug='shonen',    category=manga)
shojo,     _ = Genre.objects.get_or_create(name='Shojo',     slug='shojo',     category=manga)
seinen,    _ = Genre.objects.get_or_create(name='Seinen',    slug='seinen',    category=manga)
selfhelp,  _ = Genre.objects.get_or_create(name='Self Help', slug='self-help', category=nonfiction)

# ----- add books -----
print("Adding books...")

books_data = [
    # ----- manga -----
    {
        'title': 'One Piece Vol.1',
        'slug': 'one-piece-vol-1',
        'author': 'Eiichiro Oda',
        'category': manga,
        'genre': shonen,
        'price': 7.99,
        'stock': 15,
        'is_featured': True,
        'description': 'The beginning of Luffy\'s journey to become King of the Pirates.',
        'published_year': 1997,
        'pages': 216,
        'isbn': '978-1-56931-901-3',
    },
    {
        'title': 'Naruto Vol.1',
        'slug': 'naruto-vol-1',
        'author': 'Masashi Kishimoto',
        'category': manga,
        'genre': shonen,
        'price': 7.99,
        'stock': 10,
        'is_featured': True,
        'description': 'Follow Naruto Uzumaki, a young ninja who seeks recognition and dreams of becoming Hokage.',
        'published_year': 1999,
        'pages': 192,
        'isbn': '978-1-56931-900-6',
    },
    {
        'title': 'Attack on Titan Vol.1',
        'slug': 'attack-on-titan-vol-1',
        'author': 'Hajime Isayama',
        'category': manga,
        'genre': shonen,
        'price': 8.99,
        'stock': 8,
        'is_featured': True,
        'description': 'Humanity lives inside cities surrounded by enormous walls to protect from Titans.',
        'published_year': 2009,
        'pages': 192,
        'isbn': '978-1-61262-024-2',
    },
    {
        'title': 'Death Note Vol.1',
        'slug': 'death-note-vol-1',
        'author': 'Tsugumi Ohba',
        'category': manga,
        'genre': seinen,
        'price': 8.99,
        'stock': 12,
        'is_featured': False,
        'description': 'A high school student discovers a supernatural notebook that kills anyone whose name is written in it.',
        'published_year': 2003,
        'pages': 200,
        'isbn': '978-1-4215-0168-8',
    },
    {
        'title': 'Demon Slayer Vol.1',
        'slug': 'demon-slayer-vol-1',
        'author': 'Koyoharu Gotouge',
        'category': manga,
        'genre': shonen,
        'price': 7.99,
        'stock': 20,
        'is_featured': True,
        'description': 'Tanjiro sets out to become a demon slayer after his family is slaughtered.',
        'published_year': 2016,
        'pages': 192,
        'isbn': '978-1-9747-0954-2',
    },
    # ----- fiction -----
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'slug': 'harry-potter-philosophers-stone',
        'author': 'J.K. Rowling',
        'category': fiction,
        'genre': fantasy,
        'price': 12.99,
        'stock': 25,
        'is_featured': True,
        'description': 'A young boy discovers he is a wizard and attends Hogwarts School of Witchcraft and Wizardry.',
        'published_year': 1997,
        'pages': 223,
        'isbn': '978-0-7475-3269-9',
    },
    {
        'title': 'The Great Gatsby',
        'slug': 'the-great-gatsby',
        'author': 'F. Scott Fitzgerald',
        'category': fiction,
        'genre': mystery,
        'price': 9.99,
        'stock': 20,
        'is_featured': False,
        'description': 'A story of wealth, class, love and the American Dream in the 1920s.',
        'published_year': 1925,
        'pages': 180,
        'isbn': '978-0-7432-7356-5',
    },
    {
        'title': 'The Hobbit',
        'slug': 'the-hobbit',
        'author': 'J.R.R. Tolkien',
        'category': fiction,
        'genre': fantasy,
        'price': 11.99,
        'stock': 18,
        'is_featured': True,
        'description': 'Bilbo Baggins embarks on an unexpected journey with a group of dwarves.',
        'published_year': 1937,
        'pages': 310,
        'isbn': '978-0-261-10221-7',
    },
    # ----- non fiction -----
    {
        'title': 'Atomic Habits',
        'slug': 'atomic-habits',
        'author': 'James Clear',
        'category': nonfiction,
        'genre': selfhelp,
        'price': 14.99,
        'stock': 30,
        'is_featured': True,
        'description': 'A proven framework for improving every day by building good habits and breaking bad ones.',
        'published_year': 2018,
        'pages': 320,
        'isbn': '978-0-7352-1129-5',
    },
    {
        'title': 'Sapiens',
        'slug': 'sapiens',
        'author': 'Yuval Noah Harari',
        'category': nonfiction,
        'genre': selfhelp,
        'price': 13.99,
        'stock': 22,
        'is_featured': True,
        'description': 'A brief history of humankind from the Stone Age to the present.',
        'published_year': 2011,
        'pages': 443,
        'isbn': '978-0-06-231609-7',
    },
]

# loop through and create each book
for book_data in books_data:
    book, created = Book.objects.get_or_create(
        slug=book_data['slug'],
        defaults=book_data
    )
    if created:
        print(f'  Added: {book.title}')
    else:
        print(f'  Already exists: {book.title}')

print("Done! All data added successfully.")