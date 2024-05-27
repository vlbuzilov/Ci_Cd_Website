from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.http import JsonResponse
from shop_webapp.models import Product

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    total_price = sum(item.price for item in cart_products)
    return render(request, "cart_summary.html", {"cart_products": cart_products, "total_price": total_price})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product=product)
        response = JsonResponse({'Product Name': product.name})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        return response

def cart_update(request):
    pass

def buy_page(request):
    return render(request, "checkout.html")
