from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserProfile, ChangePasswordForm, UserInfoForm
from django.db.models import Q # for search multiple fields

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
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Info updated Successfully")
            return redirect('home')
        
        return render(request, "update_info.html", {'form': form})
    else:
        messages.success(request, "You Must Be Logged In To Update User Details")
        return redirect('home')
    
def search(request):
    # Determine if the form is filled
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the product
        searched = Product.objects.filter(name__icontains=searched)
        return render(request, "search.html", {'searched': searched})
    
    else:
        return render(request, "search.html", {})