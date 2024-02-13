from django.db import models

# Create your models here.
from django.db import models
import datetime

# Create your models here.

class category(models.Model):
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
class product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, default='', blank=True, null=True )
    image = models.ImageField(upload_to='uploads/product')
    # add sale stuff
    Is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField()
    # sale_start = models.DateTimeField(default=datetime.datetime.now)
    # sale_end = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return self.name

class order(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name