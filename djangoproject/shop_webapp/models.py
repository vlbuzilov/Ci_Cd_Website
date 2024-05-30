import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save


class Product(models.Model):
    PRODUCT_CHOICES = [
        ('laptop', 'Ноутбук'),
        ('phone', 'Телефон'),
        ('headphones', 'Навушники'),
        ('accessories', 'Аксесуари'),
    ]

    type = models.CharField(max_length=20, choices=PRODUCT_CHOICES, default='phone')
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()
    image = models.ImageField(upload_to='djangoproject/static/images')
    discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=0.00, validators=[MinValueValidator(0), MaxValueValidator(100)])
    color = models.CharField(max_length=20, default='white')
    isDiscount = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        if self.isDiscount and self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)
