from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def returning_all_products(request):
    return render(request,'shop.html')