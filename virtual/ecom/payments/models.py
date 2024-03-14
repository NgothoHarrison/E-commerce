from django.db import models
from django.contrib.auth.models import User

# shipping models
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200, null=False)
    shipping_email = models.EmailField(max_length=200, null=False)
    shipping_address1 = models.CharField(max_length=200, null=False)
    shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=200, null=False)
    pickup_point = models.CharField(max_length=200, null=False)

    # avoid prular model in admin panel

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

        def __str__(self) -> str:
            return f'Shipping Address - {str(self.id)}'

