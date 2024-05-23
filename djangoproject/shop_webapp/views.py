from django.shortcuts import render
from .models import Product

def index_page(request):
    all_products = Product.objects.all
    return render(request, 'index_.html',{'all':all_products})
def create_order(request):
    all_products = Product.objects
    return render(request, 'order_create_view.html',{'all':all_products})
