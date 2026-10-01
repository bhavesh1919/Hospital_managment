from django.urls import path
from . import views


urlpatterns = [

    path('pharma/', views.pharmacy_home, name='pharmacy_home'),

    path('checkout/', views.product_checkout, name='product_checkout'),

    path('cart/', views.cart, name='cart'),

    path(
        'add-to-cart/<int:id>/',
        views.addcart,
        name='addcart'
    ),

    path(
        'update-cart/<int:id>/',
        views.update_cart_quantity,
        name='update_cart_quantity'
    ),

    path(
        'remove-from-cart/<int:id>/',
        views.remove_cart_item,
        name='remove_cart_item'
    ),
    path(
    "update-cart/<int:id>/<str:action>/",
    views.update_cart_quantity,
    name="update_cart_quantity"
),

path("update-cart/<int:id>/<str:action>/", views.update_cart_quantity, name="update_cart_quantity"),
    
    path(
    'razorpay-payment-success/',
    views.razorpay_payment_success,
    name='razorpay_payment_success'
),


    path(
    'payment-success/',
    views.payment_success, 
    name='payment_success'
),

path(
    'my-orders/',
    views.my_orders,
    name='my_orders'
),

path(
    'order/<int:id>/',
    views.order_detail,
    name='order_detail'
),

   path(
        "verify-payment/",
        views.verify_payment,
        name="verify_payment"
    ),

path("my-orders/", views.my_orders, name="my_orders"),

]