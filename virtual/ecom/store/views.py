from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    products = product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')