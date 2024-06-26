"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from shop_webapp.views import index_page, product_list, sale_page, product_detail, login_user, logout_user, register_user, update_info, blog
from cart.views import cart_summary, cart_add, cart_delete, cart_update, buy_page
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path("", index_page, name="home"),
    path("admin/", admin.site.urls),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("update_info/", update_info, name="update_info"),
    path("products/", product_list, name="products"),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path("sale/", sale_page, name="sale"),
    path("summary/", cart_summary, name="cart_summary"),
    path("add/", cart_add, name="cart_add"),
    path("delete/", cart_delete, name="cart_delete"),
    path("update/", cart_update, name="cart_update"),
    path("checkout/", buy_page, name="checkout"),
    path("blog/", blog, name="blog"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
