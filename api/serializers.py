# suppliers/serializers.py

from django.urls import reverse
from rest_framework import serializers
from .models import InventoryTransaction, Order, OrderItem, Supplier, Category, InventoryItem # Make sure to import your Supplier model

class SupplierSerializer(serializers.ModelSerializer):
    endpoint = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = [
            "user",
            "name",
            "contact_email",
            "contact_phone",
            "address",
            "is_active",
            'path',
            'endpoint',
        ]  # You can also specify the fields explicitly, e.g., ['id', 'name', 'contact_info', ...]

    def get_endpoint(self, obj):
        # Generate the absolute API URL for the detail view
        request = self.context.get("request")
        return request.build_absolute_uri(reverse('supplier-detail', args=[obj.pk]))
    

class CatergorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"




class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating OrderItems with inventory validation."""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'supplier', 'inventory_item', 'quantity', 'order_date', 'received_date', 'status']
        read_only_fields = ['order_date']

    def validate(self, data):
        """Ensure the order quantity does not exceed available inventory before creation."""
        inventory_item = data.get('inventory_item')
        quantity = data.get('quantity')

        if inventory_item.quantity < quantity:
            raise serializers.ValidationError(
                f"Not enough inventory for item {inventory_item.name}. Available: {inventory_item.quantity}"
            )
        return data

    def create(self, validated_data):
        """Create an OrderItem and adjust the inventory quantity."""
        inventory_item = validated_data['inventory_item']
        quantity = validated_data['quantity']
        
        # Deduct inventory quantity
        inventory_item.quantity -= quantity
        inventory_item.save()
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update an OrderItem and adjust the inventory quantity if status changes to cancelled."""
        inventory_item = validated_data.get('inventory_item', instance.inventory_item)
        new_quantity = validated_data.get('quantity', instance.quantity)
        
        # Restore inventory if status changes to cancelled
        if instance.status != 'cancelled' and validated_data.get('status') == 'cancelled':
            inventory_item.quantity += instance.quantity
        elif instance.quantity != new_quantity:
            # Adjust inventory for quantity change
            inventory_item.quantity += instance.quantity - new_quantity

        inventory_item.save()
        return super().update(instance, validated_data)



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'product_record', 'ordered', 'ordered_date', 'created_at', 'updated_at']
        read_only_fields = ['ordered_date', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        

        for item_data in items_data:
            inventory_item = item_data['inventory_item']

            if inventory_item.quantity < item_data['quantity']:
                raise serializers.ValidationError(f"Not enough inventory for item {inventory_item.name}.")

            # Reduce inventory quantity
            inventory_item.quantity -= item_data['quantity']
            inventory_item.save()

            # Create OrderItem and add it to the Order
            order_item = OrderItem.objects.create(**item_data)
            order.items.add(order_item)
        order.product_record = self.updated_record(items_data)  # Set product record on creation
        order.save()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        
        # Update order fields
        instance.user = validated_data.get('user', instance.user)
        instance.product_record = validated_data.get('product_record', instance.product_record)
        instance.ordered = validated_data.get('ordered', instance.ordered)
        instance.save()

        # Process items data
        existing_items = {item.id: item for item in instance.items.all()}
        for item_data in items_data:
            item_id = item_data.get('id')
            inventory_item = item_data['inventory_item']

            if item_id and item_id in existing_items:
                # Update existing item
                order_item = existing_items.pop(item_id)
                if inventory_item.quantity + order_item.quantity < item_data['quantity']:
                    raise serializers.ValidationError(f"Not enough inventory for item {inventory_item.name}.")

                # Update inventory quantity if necessary
                inventory_item.quantity += order_item.quantity - item_data['quantity']
                inventory_item.save()

                # Update OrderItem fields
                order_item.quantity = item_data['quantity']
                order_item.save()
            else:
                # Create new OrderItem
                if inventory_item.quantity < item_data['quantity']:
                    raise serializers.ValidationError(f"Not enough inventory for item {inventory_item.name}.")

                inventory_item.quantity -= item_data['quantity']
                inventory_item.save()
                
                new_order_item = OrderItem.objects.create(**item_data)
                instance.items.add(new_order_item)

        # Remove any remaining items that weren't in the update
        for item in existing_items.values():
            item.inventory_item.quantity += item.quantity
            item.inventory_item.save()
            item.delete()

        return instance
    
    def updated_record(self, items_data):
        """Generate a product record string from the provided items data."""
        return ", ".join(str(item_data['inventory_item'].name) for item_data in items_data)


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = ['id', 'item', 'transaction_type', 'quantity', 'transaction_date', 'location', 'user']
        read_only_fields = ['transaction_date']

    def validate_quantity(self, value):
        """Ensure the transaction quantity is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def create(self, validated_data):
        """Handle creating a new inventory transaction and update inventory accordingly."""
        transaction_type = validated_data.get('transaction_type')
        quantity = validated_data.get('quantity')
        item = validated_data.get('item')

        # Adjust inventory based on transaction type
        if transaction_type == "add":
            item.quantity += quantity
        elif transaction_type == "remove":
            if item.quantity < quantity:
                raise serializers.ValidationError("Not enough stock to remove.")
            item.quantity -= quantity
        elif transaction_type == "transfer":
            # Implement transfer logic as needed
            pass
        # Save the updated inventory item
        item.save()


        return super().create(validated_data)
