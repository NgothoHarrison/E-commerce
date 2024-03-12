from django.urls import path
from . import views

urlpatterns = [
    path('payments_success/', views.payments_success, name= 'payments_success'),
]
