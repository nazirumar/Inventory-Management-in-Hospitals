from datetime import timezone
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

# 1. Supplier Model
class Supplier(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return f"/api/suppliers/{self.pk}/"

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/suppliers/{self.pk}/"
    


# 2. Category Model
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
# 3. Product Model
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="items")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey('ProductLocation', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Product Item")
        verbose_name_plural = _("Product Items")

    def __str__(self):
        return self.name

    def is_below_reorder_level(self):
        return self.quantity < self.reorder_level


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart ({self.customer.user.username})"
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    RECEIVED = "received", "Received"



class Order(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    received_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.customer.name} - {self.status}"
    

    


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE,  null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items",  null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product} in {self.order}"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def total_cost(self):
        return sum(item.quantity * item.Product_item.price_per_unit for item in self.items.all())

    def mark_as_ordered(self):
        self.ordered = True
        self.ordered_date = timezone.now()
        self.save()


# 4. ProductLocation Model
class ProductLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return self.name
    



# 7. ExpiryTracking Model
class ExpiryTracking(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="expiry_tracking")
    expiration_date = models.DateField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} - Exp. {self.expiration_date}"
    
    def is_expired(self):
        return self.expiration_date < timezone.now().date()
    


# Create your models here.

class TRANSACTION_TYPE_CHOICES(models.TextChoices):
    Add = "add", "Add"
    Remove = "remove", "Remove"
    Transfer = "transfer", "Transfer"

class ProductStockAdjustment(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPE_CHOICES.choices, 
        default=TRANSACTION_TYPE_CHOICES.Add
    )
    quantity = models.PositiveIntegerField(default=0)  # Set a default value
    transaction_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(ProductLocation, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} of {self.item.name}"

    class Meta:
        ordering = ['-transaction_date']
