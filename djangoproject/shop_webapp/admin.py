from django.contrib import admin
from .models import Product,Order,User

# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)