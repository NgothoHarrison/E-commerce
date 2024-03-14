from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserProfile, ChangePasswordForm, UserInfoForm

from payments.forms import ShippingAddressForm
from payments.models import ShippingAddress

from django.db.models import Q # for search multiple fields
import json
from cart.cart import Cart

# products page
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    # replace hyphens with space
    foo = foo.replace('-', ' ')
    # Category from the url
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        context = {'products': products, 'category': category}
        return render(request, 'category.html', context)
    except:
        messages.success(request, "Category doesn't exist")
        return redirect('home')

def home(request):
    products = Product.objects.all()
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
            # shopping cart
            current_user = Profile.objects.get(user__id=request.user.id)
            # get the saved cart
            saved_cart = current_user.old_cart 
            # convert the cart back to dictionary from string
            
            if saved_cart:
                # convert the string to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # get the cart
                cart = Cart(request)
                # loop through the dictionary and add the items to the cart
                for key, value in converted_cart.items():
                    # product = Product.objects.get(id=key)
                    cart.db_add(product=key, quantity=value)


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
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Welcome " + username + " Account Created Successfully")
            return redirect('update_info')
        else:
            messages.success(request, "Error creating account")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
       
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserProfile(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User details updated Successfully")
            return redirect('home')
        
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You Must Be Logged In To Update User Details")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # form validity
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully, Please login again")
                return redirect('login')

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)

        return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To Update User Details")
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current user shipping address
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get the user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get the shipping form
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()  # save the shipping form

            messages.success(request, "Your Info updated Successfully")
            return redirect('home')
        
        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You Must Be Logged In To Update User Details")
        return redirect('home')
    
def search(request):
    # Determine if the form is filled
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the product
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(price__icontains=searched)) # search multiple fields
        return render(request, "search.html", {'searched': searched})
    
    else:
        return render(request, "search.html", {})