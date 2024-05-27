from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import UserInfoForm
from .models import Product, Profile

from .models import Product
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


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def sale_page(request):
    sale_products = Product.objects.filter(isDiscount=True)
    for product in sale_products:
        product.actual_price = product.price * (1 - product.discount / 100)
    return render(request, 'sale.html', {'all': sale_products})


