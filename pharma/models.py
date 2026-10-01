from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth.models import User


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

    brand = models.CharField(
    max_length=150,
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



class Cart(models.Model):
    user = models.OneToOneField('auth.User',on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self. user.username


class cartiteam(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="iteams")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quentity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def get_total(self):
        return self.product.price * self.quantity

class Order(models.Model):

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    shipping = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=25
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    razorpay_order_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())




class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    product_name = models.CharField(
        max_length=255
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product_name
    
    def get_total(self):
        return self.price * self.quantity