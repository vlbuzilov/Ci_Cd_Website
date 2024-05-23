from django.shortcuts import render
from .models import Product, Order

def index_page(request):
    all_products = Product.objects.all
    return render(request, 'index_.html',{'all':all_products})
def cart_page(request):
    all_orders = Order.objects.all
    return render(request, 'cart_view.html',{'all':all_orders})
