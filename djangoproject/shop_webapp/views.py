from django.shortcuts import render
from .models import Product

def index_page(request):
    all_products = Product.objects.all
    return render(request, 'index_.html',{'all':all_products})
