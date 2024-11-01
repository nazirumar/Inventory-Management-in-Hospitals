from rest_framework import generics

from utils.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from .models import Category, InventoryItem, InventoryTransaction, Order, OrderItem, Supplier
from .serializers import CatergorySerializer, InventoryItemSerializer, InventoryTransactionSerializer, OrderItemSerializer, OrderItemSerializer, OrderSerializer, SupplierSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny  # Import this to allow unauthenticated access
from django.db import transaction
from rest_framework.exceptions import ValidationError

from rest_framework import generics, status

from rest_framework.response import Response


# View for listing all suppliers and creating a new supplier
class SupplierListCreateView(
    generics.ListCreateAPIView,
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    ):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

supplier_list_view = SupplierListCreateView.as_view()

   


# View for retrieving, updating, and deleting a specific supplier
class SupplierRetrieveUpdateDestroyView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveUpdateDestroyAPIView
    ):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

supplier_detail_view = SupplierRetrieveUpdateDestroyView.as_view()


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

category_list_view = CategoryView.as_view()



class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

inventory_list_view = InventoryItemListCreateView.as_view()


class InventoryItemUpdateCreateView(generics.RetrieveUpdateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def perform_update(self, serializer):
        """Update the inventory quantity."""
        serializer.save()
        

inventory_update_view = InventoryItemUpdateCreateView.as_view()



class InventoryItemByCategoryView(generics.ListAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]  # Optional

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return InventoryItem.objects.filter(category_id=category_id)

inventory_item_by_category = InventoryItemByCategoryView.as_view()



class OrderItemListView(generics.ListCreateAPIView):
    """List all OrderItems or create a new OrderItem."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        """Create an order item and adjust inventory quantity."""
        serializer.save()

order_item_list_view = OrderItemListView.as_view()


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific OrderItem."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_update(self, serializer):
        """Update an order item, adjusting inventory as needed."""
        serializer.save()
    
    @transaction.atomic
    def perform_destroy(self, instance):
        """Restore inventory quantity if an order item is deleted."""
        if instance.status != "cancelled":
            inventory_item = instance.inventory_item
            inventory_item.quantity += instance.quantity
            inventory_item.save()
        instance.delete()


order_item_detail_view = OrderItemDetailView.as_view()


class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Retrieve and update order details with initial data shown."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        order_item = self.get_object()
        previous_status = order_item.status
        
        # Retrieve initial data for the order
        initial_data = self.get_serializer(order_item).data

        # Update the order
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_order_item = serializer.save()

        # Restore inventory if status changes to 'cancelled'
        if previous_status != "cancelled" and updated_order_item.status == "cancelled":
            inventory_item = updated_order_item.inventory_item
            inventory_item.quantity += updated_order_item.quantity
            inventory_item.save()

        # Return the updated data along with the initial data for reference
        return Response({
            'initial_data': initial_data,  # Original data before update
            'updated_data': serializer.data  # New data after update
        }, status=status.HTTP_200_OK)
    
order_item_update_view = OrderRetrieveUpdateView.as_view()



class OrderCreateView(generics.CreateAPIView):
    """View to create a new order with multiple items."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
    
        serializer.save(user=self.request.user)

order_create = OrderCreateView.as_view()



class OrderListView(generics.ListAPIView):
    """View to list all orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


order_list = OrderListView.as_view()


class OrderDetailView(generics.RetrieveUpdateAPIView):
    """View to retrieve or update a specific order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def perform_update(self, serializer):
        order = serializer.save()
        
        # Logic to handle inventory updates if order is canceled
        if order.ordered and self.request.data.get('ordered') == 'False':
            for item in order.items.all():
                item.inventory_item.quantity += item.quantity
                item.inventory_item.save()

order_detail = OrderDetailView.as_view()


class InventoryTransactionListCreateView(generics.ListCreateAPIView):
    """View to list and create inventory transactions."""
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer

    def post(self, request, *args, **kwargs):
        """Handle creating a new inventory transaction."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


inventory_transaction_view = InventoryTransactionListCreateView.as_view()

class InventoryTransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete an inventory transaction."""
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer

inventory_transaction_detail = InventoryTransactionDetailView.as_view()
