from django.urls import path

from . import views


urlpatterns = [
    path('pharma/', views.pharmacy_home, name='pharmacy_home'),
    path('checkout/', views.product_checkout, name='product_checkout'),
    path('cart/', views.cart, name='cart'),
    path('payment-success/', views.payment_success, name='payment_success'),
]