from django.shortcuts import render


def pharmacy_home(request):
    return render(request, 'index-13.html')


def product_checkout(request):
    return render(request, 'product-checkout.html')


def cart(request):
    return render(request, 'cart.html')


def payment_success(request):
    return render(request, 'payment-success.html')