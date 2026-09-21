from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Purchase,Supplier,Cart,cartiteam
from django.contrib.auth.decorators import login_required


def pharmacy_home(request):

    products = Product.objects.all().order_by('-id')[:8]

    context = {
        'products': products,
    }


    return render(request, 'index-13.html',context)


def product_checkout(request):
    return render(request, 'product-checkout.html')

@login_required
def cart(request):

    carts, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cartiteam.objects.filter(
        cart=carts
    )

    subtotal = 0

    for item in cart_items:
        item.total = item.product.price * item.quentity
        subtotal += item.total


    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,

    }


    return render(request, 'cart.html',context)



@login_required
def update_cart_quantity(request, id, action):

    cart_item = get_object_or_404(
        cartiteam,
        id=id,
        cart__user=request.user
    )

    if action == "plus":
        cart_item.quentity += 1

    elif action == "minus":
        if cart_item.quentity > 1:
            cart_item.quentity -= 1

    cart_item.save()

    return redirect('/cart/')

@login_required
def addcart(request,id):
    product = get_object_or_404(Product,id=id)
    carts,created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = cartiteam.objects.get_or_create(
        cart=carts,
        product=product
    )

    if not created:
        cart_item.quentity += 1

        cart_item.save()

        return redirect('/cart/')



def payment_success(request):
    return render(request, 'payment-success.html')