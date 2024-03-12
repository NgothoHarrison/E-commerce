from django.shortcuts import render

# Create your views here.
def payments_success(request):
    return render(request, 'payment/payment_success.html')
