from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Purchase,Supplier,Cart,cartiteam,Order,OrderItem
from django.contrib.auth.decorators import login_required
from app1.models import Patient
from django.conf import settings
from django.contrib import messages

import razorpay


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
    # GET CART
    # ---------------------------------

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cartiteam.objects.filter(
        cart=cart
    )

    # ---------------------------------
    # CHECK EMPTY CART
    # ---------------------------------

    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("/cart/")

    # ---------------------------------
    # CALCULATE TOTAL
    # ---------------------------------

    subtotal = Decimal("0.00")

    for item in cart_items:

        item.total = (
            item.product.price *
            item.quentity
        )

        subtotal += item.total

    shipping = Decimal("25.00")
    tax = Decimal("10.00")

    total = subtotal + shipping + tax

    # ---------------------------------
    # PATIENT
    # ---------------------------------

    patient = None

    try:

        patient = Patient.objects.get(
            profile__user=request.user
        )

    except Patient.DoesNotExist:

        patient = None

    # ---------------------------------
    # CREATE ORDER ONLY ON FIRST LOAD
    # ---------------------------------

    order = None
    razorpay_order = None

    # Check if a pending checkout order already exists
    checkout_order_id = request.session.get(
        "checkout_order_id"
    )

    if checkout_order_id:

        try:

            order = Order.objects.get(
                id=checkout_order_id,
                user=request.user,
                payment_status="Pending"
            )

        except Order.DoesNotExist:

            order = None

    # ---------------------------------
    # CREATE NEW ORDER
    # ---------------------------------
    if order is None:

        order = Order.objects.create(

        user=request.user,

        first_name=(
            patient.profile.user.first_name
            if patient else ""
        ),

        last_name=(
            patient.profile.user.last_name
            if patient else ""
        ),

        email=(
            patient.profile.user.email
            if patient else ""
        ),

        phone=(
            patient.phone
            if patient else ""
        ),

        address=(
            patient.address
            if patient else ""
        ),

        city=(
            patient.city
            if patient else ""
        ),

        state=(
            patient.state
            if patient else ""
        ),

        pincode=(
            patient.pincode
            if patient else ""
        ),

        subtotal=subtotal,
        shipping=shipping,
        tax=tax,
        total=total,

        payment_status="Pending"
    )
        # ---------------------------------
        # CREATE ORDER ITEMS
        # ---------------------------------

        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                product=item.product,

                product_name=item.product.name,

                price=item.product.price,

                quantity=item.quentity,

                total=(
                    item.product.price *
                    item.quentity
                )
            )

        # ---------------------------------
        # RAZORPAY CLIENT
        # ---------------------------------

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        # ---------------------------------
        # AMOUNT IN PAISE
        # ---------------------------------

        amount_paise = int(
            total * 100
        )

        # ---------------------------------
        # CREATE RAZORPAY ORDER
        # ---------------------------------

        razorpay_order = client.order.create({

            "amount": amount_paise,

            "currency": "INR",

            "receipt":
                f"order_{order.id}",

            "payment_capture": 1
        })

        # ---------------------------------
        # SAVE RAZORPAY ORDER ID
        # ---------------------------------

        order.razorpay_order_id = (
            razorpay_order["id"]
        )

        order.save()

        # ---------------------------------
        # SAVE ORDER ID IN SESSION
        # ---------------------------------

        request.session[
            "checkout_order_id"
        ] = order.id

    else:

        # Existing pending order
        # Get its Razorpay order

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        amount_paise = int(
            total * 100
        )

        if order.razorpay_order_id:

            razorpay_order = {
                "id":
                    order.razorpay_order_id
            }

        else:

            razorpay_order = client.order.create({

                "amount": amount_paise,

                "currency": "INR",

                "receipt":
                    f"order_{order.id}",

                "payment_capture": 1
            })

            order.razorpay_order_id = (
                razorpay_order["id"]
            )

            order.save()

    # ---------------------------------
    # FINAL AMOUNT
    # ---------------------------------

    amount_paise = int(
        total * 100
    )

    # ---------------------------------
    # CONTEXT
    # ---------------------------------

    context = {

        "order": order,

        "razorpay_key":
            settings.RAZORPAY_KEY_ID,

        "razorpay_order_id":
            razorpay_order["id"],

        "amount":
            amount_paise,

        "amount_rupees":
            total,

        "patient":
            patient,

        "cart_items":
            cart_items,

        "subtotal":
            subtotal,

        "shipping":
            shipping,

        "tax":
            tax,

        "total":
            total,
    }

    return render(
        request,
        "product-checkout.html",
        context
    )


@login_required
def razorpay_payment_success(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "message": "Invalid request"
        })

    razorpay_order_id = request.POST.get(
        "razorpay_order_id"
    )

    razorpay_payment_id = request.POST.get(
        "razorpay_payment_id"
    )

    razorpay_signature = request.POST.get(
        "razorpay_signature"
    )

    if not razorpay_order_id:

        return JsonResponse({
            "success": False,
            "message": "Razorpay Order ID missing"
        })

    # ---------------------------------
    # GET ORDER
    # ---------------------------------

    order = get_object_or_404(
        Order,
        razorpay_order_id=razorpay_order_id,
        user=request.user
    )

    # ---------------------------------
    # VERIFY PAYMENT
    # ---------------------------------

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        client.utility.verify_payment_signature({

            "razorpay_order_id":
                razorpay_order_id,

            "razorpay_payment_id":
                razorpay_payment_id,

            "razorpay_signature":
                razorpay_signature
        })

    except razorpay.errors.SignatureVerificationError:

        order.payment_status = "Failed"

        order.save()

        return JsonResponse({

            "success": False,

            "message":
                "Payment verification failed."
        })

    # ---------------------------------
    # PAYMENT SUCCESS
    # ---------------------------------

    order.razorpay_payment_id = (
        razorpay_payment_id
    )

    order.payment_status = "Paid"

    order.save()

    # ---------------------------------
    # CLEAR CART
    # ---------------------------------

    cart = Cart.objects.get(
        user=request.user
    )

    cartiteam.objects.filter(
        cart=cart
    ).delete()

    return JsonResponse({

        "success": True,

        "redirect_url":
            "/payment-success/"
    })



def payment_success(request):

    return render(
        request,
        'payment-success.html'
    )





import razorpay

from django.conf import settings
from django.http import JsonResponse

import razorpay

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem


@csrf_exempt
@login_required
def verify_payment(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=405)

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
        return JsonResponse({
            "status": "error",
            "message": "Payment information is missing"
        }, status=400)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        # Verify Razorpay payment
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })

        # ------------------------------------------------
        # PAYMENT SUCCESS
        # ------------------------------------------------

        # Get the pending order created during checkout
        order_id = request.session.get("checkout_order_id")

        if not order_id:
            return JsonResponse({
                "status": "error",
                "message": "Order information not found"
            }, status=400)

        order = Order.objects.get(
            id=order_id,
            user=request.user
        )

        # Save Razorpay details
        order.razorpay_order_id = razorpay_order_id
        order.razorpay_payment_id = razorpay_payment_id
        order.payment_status = "Paid"
        order.order_status = "Confirmed"

        order.save()

        # Remove checkout order from session
        request.session.pop("checkout_order_id", None)

        return JsonResponse({
            "status": "success",
            "message": "Payment successful",
            "redirect_url": "/my-orders/"
        })

    except razorpay.errors.SignatureVerificationError:

        return JsonResponse({
            "status": "error",
            "message": "Payment verification failed"
        }, status=400)

    except Order.DoesNotExist:

        return JsonResponse({
            "status": "error",
            "message": "Order not found"
        }, status=404)

    except Exception as e:

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)



@login_required
def cart(request):
    products =Product.objects.all()

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

    if cart_items.exists():
        shipping = 25
        tax = 10
    else:
        shipping = 0
        tax = 0

    total = subtotal + shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        "products": products,
    }

    return render(
        request,
        'cart.html',
        context
    )
@login_required
def update_cart_quantity(request, id, action):

    item = get_object_or_404(cartiteam, id=id)

    if action == "increase":
        item.quentity += 1
        item.save()

    elif action == "decrease":
        if item.quentity > 1:
            item.quentity -= 1
            item.save()
        else:
            item.delete()

    return redirect("cart")


# @login_required
# def update_cart_quantity(request, id):

#     cart_item = get_object_or_404(
#         cartiteam,
#         id=id,
#         cart__user=request.user
#     )

#     if request.method == "POST":

#         quantity = int(request.POST.get("quantity", 1))

#         if quantity < 1:
#             quantity = 1

#         cart_item.quentity = quantity
#         cart_item.save()

#         item_total = cart_item.product.price * cart_item.quentity

#         return JsonResponse({
#             "success": True,
#             "quantity": cart_item.quentity,
#             "item_total": float(item_total),
#         })

#     return JsonResponse({
#         "success": False
#     })





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



@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my-orders.html',
        {
            'orders': orders
        }
    )

@login_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    order_items = order.items.all()

    return render(
        request,
        'order-detail.html',
        {
            'order': order,
            'order_items': order_items
        }
    )



## order after pyment view
@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related("items").order_by("-created_at")

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders
        }
    )