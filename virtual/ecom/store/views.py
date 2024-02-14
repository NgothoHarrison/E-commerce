from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

# Create your views here.
def home(request):
    products = product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "Error logging in - please try again")
            return redirect('login')


    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Account was created for " + username)
            return redirect('login')
        else:
            messages.success(request, "Error creating account")
            return redirect('home')
    else:
        return render(request, 'register.html', {'form': form})
        # username = request.POST['username']
        # email = request.POST['email']
        # password = request.POST['password']
        # user = User.objects.create_user(username, email, password)
        # user.save()
        # messages.success(request, "You have registered successfully")
        # return redirect('home')

    # return render(request, 'register.html', {})