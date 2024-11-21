# suppliers/urls.py
from django.urls import path


from .views import (
    supplier_detail_view,
    supplier_list_view,
    supplier_delete_view,

    category_list_view,
    category_delete_view,
    category_update_view,

    product_list_view,
    product_item_by_category,
    product_update_view,
    product_delete_view,


    add_to_cart_view,
    cart_detail_view,
    cart_item_added_view,
    cart_item_view,
    checkout_view,
    
    order_item_list_view,
    order_item_create_view,
    order_item_update_view,
    order_item_delete_view,

    order_create,
    order_list_view,
    order_update_view,
    order_delete_views,
   
    product_stock_view,
    product_stock_create_view,
    product_stock_update,
    product_stock_delete,
  
    location_list_view,
)

urlpatterns = [

    path("categories/", category_list_view, name="category-list"),  # For retrieving, updating, and deleting a supplier
    path("categories/<int:pk>/delete", category_delete_view, name="category-delete"),  # For retrieving, updating, and deleting a supplier
    path("categories/<int:pk>/update", category_update_view, name="category-delete"),  # For retrieving, updating, and deleting a supplier
    
    path("suppliers/<int:pk>/update", supplier_detail_view, name="supplier-detail"),  # For retrieving, updating, and deleting a supplier
    path("suppliers/<int:pk>/delete", supplier_delete_view, name="supplier-delete"),  # For retrieving, updating, and deleting a supplier
    path("suppliers/", supplier_list_view, name="supplie-list"),  # For retrieving, updating, and deleting a supplier
    
    path("locations/", location_list_view, name="location-list"),  # For retrieving, updating, and deleting a supplier
    

    path("inventories/", product_list_view, name="product-list"),  # For retrieving, updating, and deleting a supplier
    path("product/category/<int:category_id>/", product_item_by_category, name="product-by-category",),
    path('product/<int:pk>/update', product_update_view, name='product-update'),
    path('product/<int:pk>/delete', product_delete_view, name='product-delete'),
     
    path('carts/', add_to_cart_view, name='cart-list-create'),
    path('carts/<int:pk>/', cart_detail_view, name='cart-detail'),
    path('cart-items/add/', cart_item_added_view, name='cart-detail'),
    path('cart-items', cart_item_view, name='cart-detail'),
    path('checkout', checkout_view, name='checkout-items'),

    path('orderitems/', order_item_list_view, name='orderitem-list'),
    path('orderitems/create', order_item_create_view, name='orderitem-create'),
    path('orderitems/<int:pk>/update', order_item_update_view, name='orderitem-detail'),
    path('orderitems/<int:pk>/delete', order_item_delete_view, name='orderitem-delete'),

    path("orders/", order_list_view, name="order-list"),
    path("orders/create", order_create, name="order-create"),
    path("orders/<int:pk>/update", order_update_view, name="order-update"),
    path("orders/<int:pk>/delete", order_delete_views, name="order-delete"),


    path('product/stock', product_stock_view, name='product-stock-list-create'),
    path('product/stock/create', product_stock_create_view, name='product-stock-list-create'),
    path('product/stock/<int:pk>/update', product_stock_update, name='product-stock-update'),
    path('product/stock/<int:pk>/delete', product_stock_delete, name='product-stock-delete'),

]
