from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Purchase,Supplier,Cart,cartiteam
from django.contrib.auth.decorators import login_required
from app1.models import Patient




from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render











def pharmacy_home(request):

    products = Product.objects.all().order_by('-id')[:8]

    context = {
        'products': products,
    }


    return render(request, 'index-13.html',context)

@login_required
def product_checkout(request):



    # ---------------------------------
    # CART
    # ---------------------------------

    cart, created = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None
    )

    cart_items = cartiteam.objects.filter(
        cart=cart
    )


    # ---------------------------------
    # CALCULATE TOTAL
    # ---------------------------------

    subtotal = 0

    for item in cart_items:

        item.total = (
            item.product.price *
            item.quentity
        )

        subtotal += item.total


    shipping = 25
    tax = 10

    total = subtotal + shipping + tax


    # ---------------------------------
    # PATIENT
    # ---------------------------------

    patient = None

    if request.user.is_authenticated:

        try:

            patient = Patient.objects.get(
                profile__user=request.user
            )

        except Patient.DoesNotExist:

            patient = None


    # ---------------------------------
    # FORM SUBMIT
    # ---------------------------------

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        payment_method = request.POST.get(
            "payment_method"
        )


        # ---------------------------------
        # LOGGED-IN PATIENT
        # ---------------------------------

        if request.user.is_authenticated and patient:

            # UPDATE EXISTING PATIENT
            #
            # IMPORTANT:
            # Change these field names if your
            # Patient model uses different names.

            patient.first_name = first_name
            patient.last_name = last_name
            patient.email = email
            patient.phone = phone
            patient.address = address
            patient.city = city
            patient.state = state
            patient.pincode = pincode

            patient.save()


        # ---------------------------------
        # GUEST PATIENT
        # ---------------------------------

        else:

            # IMPORTANT:
            # Change these field names to exactly
            # match your Patient model.

            patient = Patient.objects.create(

                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode,

            )


        # ---------------------------------
        # PAYMENT
        # ---------------------------------

        print("Payment Method:", payment_method)

        print("Subtotal:", subtotal)
        print("Shipping:", shipping)
        print("Tax:", tax)
        print("Total:", total)


        # ---------------------------------
        # SUCCESS
        # ---------------------------------

        return redirect("payment_success")


    # ---------------------------------
    # GET FORM VALUES
    # ---------------------------------

    context = {

        "cart_items": cart_items,

        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total": total,

        "patient": patient,

    }


   

    return render(request, 'product-checkout.html',context)

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

    shipping = 25
    tax = 10

    total = subtotal + shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }

    return render(
        request,
        'cart.html',
        context
    )


@login_required
def update_cart_quantity(request, id):

    cart_item = get_object_or_404(
        cartiteam,
        id=id,
        cart__user=request.user
    )

    if request.method == "POST":

        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        cart_item.quentity = quantity
        cart_item.save()

        item_total = cart_item.product.price * cart_item.quentity

        return JsonResponse({
            "success": True,
            "quantity": cart_item.quentity,
            "item_total": float(item_total),
        })

    return JsonResponse({
        "success": False
    })





@login_required
def addcart(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    carts, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = cartiteam.objects.get_or_create(
        cart=carts,
        product=product
    )

    if not created:

        cart_item.quentity += 1
        cart_item.save()

    return redirect('/cart/')


@login_required
def remove_cart_item(request, id):

    cart_item = get_object_or_404(
        cartiteam,
        id=id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect('/cart/')