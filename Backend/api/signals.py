from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import OrderItem, Order, Status, ProductStockAdjustment, TRANSACTION_TYPE_CHOICES

@receiver(pre_save, sender=OrderItem)
def adjust_product_quantity_on_create_or_update(sender, instance, **kwargs):
    """
    Adjust product quantity on OrderItem creation or update.
    """
    print("Helllo")
    if instance.pk:  # Updating an existing OrderItem
        previous_instance = OrderItem.objects.get(pk=instance.pk)
        product = instance.product

        # Adjust product quantity for changes in OrderItem quantity
        if previous_instance.quantity != instance.quantity:
            product.quantity += previous_instance.quantity - instance.quantity
            product.save()

    else:  # Creating a new OrderItem
        product = instance.product
        product.quantity -= instance.quantity
        product.save()

@receiver(pre_delete, sender=OrderItem)
def restore_product_quantity_on_delete(sender, instance, **kwargs):
    print("delete")
    """
    Restore product quantity when an OrderItem is deleted.
    """
    product = instance.product
    product.quantity += instance.quantity
    product.save()

@receiver(pre_save, sender=Order)
def handle_order_status_change(sender, instance, **kwargs):
    """
    Adjust product quantities when Order status changes, including:
    - Restoring quantities for 'cancelled'
    - Reversing quantities for 'pending'
    """
    if instance.pk:  # Only process updates
        previous_instance = Order.objects.get(pk=instance.pk)

        # Restore product quantities when status changes to 'cancelled'
        if previous_instance.status != instance.status and instance.status == Status.CANCELLED:
            for item in instance.items.all():
                product = item.product
                product.quantity += item.quantity
                product.save()

        # Reverse product quantities when status changes back to 'pending'
        elif previous_instance.status != instance.status and instance.status == Status.PENDING:
            for item in instance.items.all():
                product = item.product
                product.quantity -= item.quantity
                product.save()


@receiver(post_save, sender=ProductStockAdjustment)
def product_update(sender, instance, created, **kwargs):
    """
    Update product quantity after a ProductTransaction is created.
    """
    if created:
        if instance.transaction_type == TRANSACTION_TYPE_CHOICES.Add:
            product = instance.item
            product.quantity += instance.quantity
            product.save()
            if instance.quantity < 0:
                raise ValueError("Product quantity cannot be negative.")

        elif instance.transaction_type == TRANSACTION_TYPE_CHOICES.Remove:
            product = instance.item
            if instance.quantity > product.quantity:
                raise ValueError("Not enough stock to remove.")
            product.quantity -= instance.quantity
            product.save()
            if product.quantity < 0:
                raise ValueError("Product quantity cannot be negative.")
        
        elif instance.transaction_type == TRANSACTION_TYPE_CHOICES.Transfer:
            # Ensure quantity is not negative before making any updates
            if instance.quantity < 0:
                raise ValueError("Quantity cannot be negative.")

            # Update product quantity
            product = instance.item
            location = instance.location
            location = location
            product.quantity += instance.quantity

            product.save()
            location.save()
