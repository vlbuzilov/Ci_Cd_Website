from django.shortcuts import render
from .models import Product, Order


def index_page(request):
    return render(request, 'index.html')


def product_page(request):
    query = request.GET.get('name_contains', '')
    sort = request.GET.get('sort', 'none')

    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'products.html', {'all_products': products})




def cart_page(request):
    all_orders = Order.objects.all
    return render(request, 'cart_view.html', {'all': all_orders})

def sale_page(request):
    sale_products = Product.objects.filter(isDiscount=True)
    for product in sale_products:
        product.actual_price = product.price * (1 - product.discount / 100)
    return render(request, 'sale.html',{'all':sale_products})
