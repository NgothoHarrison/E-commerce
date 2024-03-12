from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/', views.payments_success, name= 'payment_success'),
]
