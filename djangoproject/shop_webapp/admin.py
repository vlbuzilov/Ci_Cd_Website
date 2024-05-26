from django.contrib import admin
from django.contrib.auth.models import User

from .models import Product, Profile

admin.site.register(Product)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "email", "first_name", "last_name"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
