from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()

# 1. Supplier Model
class Supplier(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
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
    

# 3. InventoryItem Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="items")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey('InventoryLocation', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Inventory Item")
        verbose_name_plural = _("Inventory Items")

    def __str__(self):
        return self.name

    def is_below_reorder_level(self):
        return self.quantity < self.reorder_level
    

class OrderItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="order_items")
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("ordered", "Ordered"),
            ("received", "Received"),
            ("cancelled", "Cancelled")
        ],
        default="ordered"
    )

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.inventory_item.name} ({self.quantity}) - {self.status}"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    items = models.ManyToManyField(OrderItem, related_name='orders')
    product_record = models.TextField(null=True, blank=True, help_text="Record of the ordered products and quantities.")
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user}"


    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def total_cost(self):
        return sum(item.quantity * item.inventory_item.price_per_unit for item in self.items.all())

    def mark_as_ordered(self):
        self.ordered = True
        self.ordered_date = timezone.now()
        self.save()


# 4. InventoryLocation Model
class InventoryLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return self.name
    



# 7. ExpiryTracking Model
class ExpiryTracking(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="expiry_tracking")
    expiration_date = models.DateField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} - Exp. {self.expiration_date}"
    
    def is_expired(self):
        return self.expiration_date < timezone.now().date()
    


# Create your models here.
class InventoryTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("add", "Add Stock"),
        ("remove", "Remove Stock"),
        ("transfer", "Transfer Stock"),
    ]
    
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(InventoryLocation, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Tracking who made the transaction
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.name}"
