# suppliers/urls.py
from django.urls import path


from .views import (
    supplier_detail_view,
    supplier_list_view,
    category_list_view,
    inventory_list_view,
    inventory_item_by_category,
    order_item_list_view,
    order_item_detail_view,
    order_item_update_view,
    order_create,
    order_list,
    order_detail,
    inventory_transaction_view,
    inventory_transaction_detail
)

urlpatterns = [
    path("supplier-list", supplier_list_view, name="supplier-list-create"),  # For listing and creating suppliers
    path("<int:pk>/", supplier_detail_view, name="supplier-detail"),  # For retrieving, updating, and deleting a supplier
    path("category-list", category_list_view, name="category-list"),  # For retrieving, updating, and deleting a supplier
    
    path("inventory-list", inventory_list_view, name="inventory-list"),  # For retrieving, updating, and deleting a supplier
    path("inventory/category/<int:category_id>/", inventory_item_by_category, name="inventory-by-category",),
    
    path('order-items/', order_item_list_view, name='orderitem-list'),
    path('order-items/<int:pk>/', order_item_detail_view, name='orderitem-detail'),

    path("orders/", order_list, name="order-list"),
    path("orders/create/", order_create, name="order-create"),
    path("orders/<int:pk>/", order_detail, name="order-detail"),

    path('transactions/', inventory_transaction_view, name='inventory-transaction-list-create'),
    path('transactions/<int:pk>/', inventory_transaction_detail, name='inventory-transaction-detail'),

]
