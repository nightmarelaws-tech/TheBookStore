from django.shortcuts import render

def homepage(request):
    """Temporary homepage - just to test header and footer."""
    return render(request, 'store/homepage.html', {
        'page_title': 'The Book Merchant',
    })