from django.contrib import admin
from .models import Category, customer, Product, order, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(customer)
admin.site.register(Product)
admin.site.register(order)
admin.site.register(Profile)

# Mix profile info with user info

class ProfileInline(admin.StackedInline):
    model = Profile

# Extend user model
    
class UserAdmin(admin.ModelAdmin):
    model = User
    field = [ 'username', 'email', 'first_name', 'last_name', 'password']
    inlines = [ProfileInline]

# Unregister old user admin
admin.site.unregister(User)

# Register new user admin
admin.site.register(User, UserAdmin)