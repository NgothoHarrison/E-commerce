
# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.name 
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, default='', blank=True, null=True )
    image = models.ImageField(upload_to='uploads/product')
    # add sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField()
    # sale_start = models.DateTimeField(default=datetime.datetime.now)
    # sale_end = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return self.name

class order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
    
# Create customer profile
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length = 20, blank = True)
    address1 = models.TextField(max_length = 255, blank = True)
    address2 = models.TextField(max_length = 255, blank = True)
    city = models.CharField(max_length = 255, blank = True)
    state = models.CharField(max_length = 255, blank = True)
    country = models.CharField(max_length = 255, blank = True)
    zip = models.CharField(max_length = 255, blank = True)
    old_cart = models.CharField(max_length = 500, blank = True, null=True)

    def __str__(self):
        return self.user.username
    

# Create a profile by default when a user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)
    