

# Register your models here.
from django.contrib import admin
from .models import Category, Supplier, Product, Purchase, Sale,Order,OrderItem


admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Order)
admin.site.register(OrderItem)