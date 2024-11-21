from django.shortcuts import get_object_or_404
from rest_framework import generics

from utils.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from .models import Cart, CartItem, Category, Product, ProductLocation, ProductStockAdjustment, Order, OrderItem, Supplier
from .serializers import CartItemSerializer, CartSerializer, CatergorySerializer, ProductSerializer, ProductStockAdjustmentSerializer, LocationSerializer, OrderItemSerializer, OrderItemSerializer, OrderSerializer, SupplierSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny  # Import this to allow unauthenticated access
from django.db import transaction
from rest_framework.views import APIView

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

supplier_list_view = SupplierListCreateView.as_view()

   


# View for retrieving, updating, and deleting a specific supplier
class SupplierUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView
    ):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

supplier_detail_view = SupplierUpdateAPIView.as_view()



class SupplierDeleteAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView
    ):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

supplier_delete_view = SupplierDeleteAPIView.as_view()




class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access

category_list_view = CategoryView.as_view()




class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access
    lookup_field = 'pk'
    
category_update_view = CategoryUpdateView.as_view()


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CatergorySerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access
    lookup_field = 'pk'

category_delete_view = CategoryDeleteView.as_view()

# class SupplierView(generics.ListCreateAPIView):
#     queryset = Supplier.objects.all()
#     serializer_class = CatergorySerializer
#     permission_classes = [AllowAny]  # Allow unauthenticated access

#     def perform_create(self, serializer):
#         return super().perform_create(serializer)

# supplier_list_view = SupplierView.as_view()


class ProductLocationView(generics.ListCreateAPIView):
    queryset = ProductLocation.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

location_list_view = ProductLocationView.as_view()
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access

product_list_view = ProductListCreateView.as_view()


class ProductUpdateCreateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def perform_update(self, serializer):
        """Update the Product quantity."""
        serializer.save()
        
product_update_view = ProductUpdateCreateView.as_view()



class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access


product_delete_view = ProductDeleteView.as_view()


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer')
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

add_to_cart_view = CartListCreateView.as_view()



class CartDetailView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
cart_detail_view = CartDetailView.as_view()


class CartItemAddView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        cart_item, created = CartItem.objects.update_or_create(
            cart_id=cart_id,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

cart_item_added_view = CartItemAddView.as_view()



class CartItemDetailView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]  # Optional

cart_item_view = CartItemDetailView.as_view()





class CheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get("customer")
        try:
            # Get the cart for the customer
            cart = Cart.objects.get(customer_id=customer_id)
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items.exists():
                return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Create an order
            order = Order.objects.create(customer=cart.customer)

            # Transfer items from cart to order
            for cart_item in cart_items:
                OrderItem.objects.create(
                    user=request.user,
                    product=cart_item.product,
                    order=order,
                    quantity=cart_item.quantity,
                    total_price=cart_item.product.price_per_unit * cart_item.quantity,  # Assuming `Product` has a `price` field
                )

            # Delete the cart and its items
            cart_items.delete()
            cart.delete()

            return Response({"message": "Order created successfully.", "order_id": order.id}, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        

checkout_view = CheckoutView.as_view()


class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Optional

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id)

product_item_by_category = ProductByCategoryView.as_view()



class OrderItemListView(generics.ListAPIView):
    """List all OrderItems or create a new OrderItem."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

order_item_list_view = OrderItemListView.as_view()

class OrderItemCreateView(generics.CreateAPIView):
    """List all OrderItems or create a new OrderItem."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        """Create an order item and adjust Product quantity."""
        serializer.save()

order_item_create_view = OrderItemCreateView.as_view()




class OrderRetrieveUpdateView(generics.UpdateAPIView):
    """Retrieve and update order details with initial data shown."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_update(self, serializer):
        """Update an order item, adjusting Product as needed."""
        serializer.save()

order_item_update_view = OrderRetrieveUpdateView.as_view()


class OrderItemDeleteView(generics.DestroyAPIView):
    """List all OrderItems or create a new OrderItem."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


order_item_delete_view = OrderItemDeleteView.as_view()



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


order_list_view = OrderListView.as_view()


class OrderUpdateView(generics.RetrieveUpdateAPIView):
    """View to retrieve or update a specific order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


order_update_view = OrderUpdateView.as_view()


class OrderDeleteView(generics.DestroyAPIView):
    """View to list all orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


order_delete_views = OrderDeleteView.as_view()

# ======================  ProductStockAdjustment =============================

class ProductStockAdjustmentListCreateView(generics.ListAPIView):
    """View to list and create Product transactions."""
    queryset = ProductStockAdjustment.objects.all()
    serializer_class = ProductStockAdjustmentSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access

product_stock_view = ProductStockAdjustmentListCreateView.as_view()

class ProductStockAdjustmentCreateView(generics.CreateAPIView):
    """View to list and create Product transactions."""
    queryset = ProductStockAdjustment.objects.all()
    serializer_class = ProductStockAdjustmentSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access

    def perform_create(self, serializer):
        """Handle creating a new Product transaction."""
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

product_stock_create_view = ProductStockAdjustmentCreateView.as_view()

class ProductTransactionUpdateView(generics.UpdateAPIView):
    """View to retrieve, update, or delete an Product transaction."""
    queryset = ProductStockAdjustment.objects.all()
    serializer_class = ProductStockAdjustmentSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access

    def perform_update(self, serializer):
        """Handle updating a Product transaction."""
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

product_stock_update = ProductTransactionUpdateView.as_view()


class ProductTransactionDeleteView(generics.DestroyAPIView):
    """View to retrieve, update, or delete an Product transaction."""
    queryset = ProductStockAdjustment.objects.all()
    serializer_class = ProductStockAdjustmentSerializer
    permission_classes = [IsAuthenticated]  # Allow unauthenticated access

product_stock_delete = ProductTransactionDeleteView.as_view()
