# suppliers/serializers.py

from django.urls import reverse
from rest_framework import serializers
from .models import (
    Cart,
    CartItem,
    ProductLocation,
    ProductStockAdjustment,
    Order,
    OrderItem,
    Supplier,
    Category,
    Product,
)  # Make sure to import your Supplier model


class SupplierSerializer(serializers.ModelSerializer):
    endpoint = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = [
            'id',
            "user",
            "name",
            "contact_email",
            "contact_phone",
            "address",
            "is_active",
            "path",
            "endpoint",
        ]  # You can also specify the fields explicitly, e.g., ['id', 'name', 'contact_info', ...]

    def get_endpoint(self, obj):
        # Generate the absolute API URL for the detail view
        request = self.context.get("request")
        return request.build_absolute_uri(reverse("supplier-detail", args=[obj.pk]))


class CatergorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"



class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLocation
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'supplier',
            'quantity',
            'reorder_level',
            'price_per_unit',
            'location',
            'category',
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_name', 'quantity', 'added_at']
        read_only_fields = ['cart', 'added_at']

        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating OrderItems with Product validation."""

    class Meta:
        model = OrderItem
        fields = [
            "id",
            'user',
            'product',
            'order',
            'quantity',
            'total_price',
            'created_at',
            'updated_at',
        ]
    #     read_only_fields = ["order_date"]

    # def validate(self, data):
    #     """Ensure the order quantity does not exceed available Product before creation."""
    #     Product_item = data.get("Product_item")
    #     quantity = data.get("quantity")

    #     if Product_item.quantity < quantity:
    #         raise serializers.ValidationError(
    #             f"Not enough Product for item {Product_item.name}. Available: {Product_item.quantity}"
    #         )
    #     return data

    # def create(self, validated_data):
    #     """Create an OrderItem and adjust the Product quantity."""
    #     Product_item = validated_data["Product_item"]
    #     quantity = validated_data["quantity"]

    #     # Deduct Product quantity
    #     Product_item.quantity -= quantity
    #     Product_item.save()

    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     """Update an OrderItem and adjust the Product quantity if status changes to cancelled."""
    #     Product_item = validated_data.get("Product_item", instance.Product_item)
    #     new_quantity = validated_data.get("quantity", instance.quantity)

    #     # Restore Product if status changes to cancelled
    #     if (
    #         instance.status != "cancelled"
    #         and validated_data.get("status") == "cancelled"
    #     ):
    #         Product_item.quantity += instance.quantity
    #     elif instance.quantity != new_quantity:
    #         # Adjust Product for quantity change
    #         Product_item.quantity += instance.quantity - new_quantity

    #     Product_item.save()
    #     return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            'customer',
            'status',
            'order_date',
            'complete',
            'received_date',
            "created_at",
        ]
        read_only_fields = ["ordered_date", "created_at", "updated_at"]

    # def create(self, validated_data):
    #     items_data = validated_data.pop("items", [])
    #     order = Order.objects.create(**validated_data)

    #     for item_data in items_data:
    #         Product_item = item_data["Product_item"]

    #         if Product_item.quantity < item_data["quantity"]:
    #             raise serializers.ValidationError(
    #                 f"Not enough Product for item {Product_item.name}."
    #             )

    #         # Reduce Product quantity
    #         Product_item.quantity -= item_data["quantity"]
    #         Product_item.save()

    #         # Create OrderItem and add it to the Order
    #         order_item = OrderItem.objects.create(**item_data)
    #         order.items.add(order_item)
    #     order.product_record = self.updated_record(
    #         items_data
    #     )  # Set product record on creation
    #     order.save()
    #     return order

    # def update(self, instance, validated_data):
    #     items_data = validated_data.pop("items", [])

    #     # Update order fields
    #     instance.user = validated_data.get("user", instance.user)
    #     instance.product_record = validated_data.get(
    #         "product_record", instance.product_record
    #     )
    #     instance.ordered = validated_data.get("ordered", instance.ordered)
    #     instance.save()

    #     # Process items data
    #     existing_items = {item.id: item for item in instance.items.all()}
    #     for item_data in items_data:
    #         item_id = item_data.get("id")
    #         Product_item = item_data["Product_item"]

    #         if item_id and item_id in existing_items:
    #             # Update existing item
    #             order_item = existing_items.pop(item_id)
    #             if (
    #                 Product_item.quantity + order_item.quantity
    #                 < item_data["quantity"]
    #             ):
    #                 raise serializers.ValidationError(
    #                     f"Not enough Product for item {Product_item.name}."
    #                 )

    #             # Update Product quantity if necessary
    #             Product_item.quantity += order_item.quantity - item_data["quantity"]
    #             Product_item.save()

    #             # Update OrderItem fields
    #             order_item.quantity = item_data["quantity"]
    #             order_item.save()
    #         else:
    #             # Create new OrderItem
    #             if Product_item.quantity < item_data["quantity"]:
    #                 raise serializers.ValidationError(
    #                     f"Not enough Product for item {Product_item.name}."
    #                 )

    #             Product_item.quantity -= item_data["quantity"]
    #             Product_item.save()

    #             new_order_item = OrderItem.objects.create(**item_data)
    #             instance.items.add(new_order_item)

    #     # Remove any remaining items that weren't in the update
    #     for item in existing_items.values():
    #         item.Product_item.quantity += item.quantity
    #         item.Product_item.save()
    #         item.delete()

    #     return instance

    # def updated_record(self, items_data):
    #     """Generate a product record string from the provided items data."""
    #     return ", ".join(
    #         str(item_data["Product_item"].name) for item_data in items_data
    #     )


class ProductStockAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStockAdjustment
        fields = [
            "id",
            "item",
            "transaction_type",
            "quantity",
            "transaction_date",
            "location",
            "user",
        ]
        read_only_fields = ["transaction_date"]

    def validate_quantity(self, value):
        """Ensure the transaction quantity is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
