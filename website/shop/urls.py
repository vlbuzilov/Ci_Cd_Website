from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.returning_all_products),
]