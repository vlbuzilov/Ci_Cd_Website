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


from shop_webapp.views import index_page, cart_page, product_page, sale_page, product_detail

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index_page),
    path("admin/", admin.site.urls),
    path("products/", product_page, name="products"),
    path("cart/", cart_page),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path("sale/",sale_page,name="sale")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
