from django.db import models
from django.contrib.auth.models import User

# shipping models
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, null=False)
    