from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=True)



    shipping_full_name = models.CharField(max_length=200, null=False)
    shipping_email = models.EmailField(max_length=200, null=False)
    shipping_address1 = models.CharField(max_length=200, null=False)
    shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
    shipping_city = models.CharField(max_length=200, null=False)
    pickup_point = models.CharField(max_length=200, null=False)
       