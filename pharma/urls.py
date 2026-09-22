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

]