from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import UserInfoForm
from .models import Product, Profile

def index_page(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged')
            return redirect('home')
        else:
            messages.error(request, 'There was an error, please try again')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, 'You have successfully registered')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')


def update_info(request):
    user = request.user
    current_user_profile = Profile.objects.get(user_id=user.id)
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=current_user_profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been updated')
            return redirect('home')
    else:
        form = UserInfoForm(instance=current_user_profile, user=user)

    return render(request, 'update_info.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def product_list(request):
    products = Product.objects.all()

    # Фільтр за типом продукту
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(type=product_type)

    # Пошук за ім'ям продукту
    name_contains = request.GET.get('name_contains')
    if name_contains:
        products = products.filter(name__icontains=name_contains)

    # Фільтр за кольором
    product_color = request.GET.get('color')
    if product_color:
        products = products.filter(color=product_color)

    # Сортування за ціною
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # Отримати доступні кольори для фільтрації
    available_colors = Product.objects.values_list('color', flat=True).distinct()

    context = {
        'all_products': products,
        'available_colors': available_colors,
    }
    return render(request, 'products.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    discounted_price = product.get_discounted_price()
    return render(request, 'product_detail.html', {'product': product, 'discounted_price': discounted_price})


def sale_page(request):
    # Отримання продуктів на розпродажі
    sale_products = Product.objects.filter(isDiscount=True)

    # Обчислення актуальної ціни
    for product in sale_products:
        product.actual_price = product.price * (1 - product.discount / 100)

    # Отримання доступних кольорів
    available_colors = Product.objects.filter(isDiscount=True).values_list('color', flat=True).distinct()

    # Фільтрація за типом продукту
    product_type = request.GET.get('type')
    if product_type:
        sale_products = sale_products.filter(type=product_type)

    # Пошук за ім'ям продукту
    name_contains = request.GET.get('name_contains')
    if name_contains:
        sale_products = sale_products.filter(name__icontains=name_contains)

    # Фільтрація за кольором
    product_color = request.GET.get('color')
    if product_color:
        sale_products = sale_products.filter(color=product_color)

    # Сортування за ціною
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        sale_products = sale_products.order_by('price')
    elif sort == 'price_desc':
        sale_products = sale_products.order_by('-price')

    return render(request, 'sale.html', {'all': sale_products, 'available_colors': available_colors})
