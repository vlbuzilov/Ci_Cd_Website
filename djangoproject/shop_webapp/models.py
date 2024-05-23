import uuid

from django.db import models

"""
    Product - модель саме для відображення продукту в шопі
    User - модель для авторизації/реєстрації юзера
    Order - модель для відображення замовлення
"""


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images')
    isDiscount = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    description = models.TextField()

    def __str__(self):
        return str(self.id)
