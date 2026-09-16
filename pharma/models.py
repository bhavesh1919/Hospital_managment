from django.db import models

# Create your models here.
from django.db import models
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=150
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='pharmacy/products/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Purchase(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    purchase_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product.name


class Sale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sale_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product.name