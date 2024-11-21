# Product/admin.py

from datetime import datetime
from django.contrib import admin
from .models import Category, Customer, OrderItem, Product, Cart, CartItem, ProductStockAdjustment ,ProductLocation,ExpiryTracking, Order, Supplier

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category', 'supplier', 'price_per_unit', 'quantity', 'reorder_level', 'location')
    search_fields = ('name', 'supplier__name', 'category__name')
    list_filter = ('category', 'supplier', 'location')
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name','phone']


# suppliers/admin.py


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_related_objects', 'customer',)
    search_fields = ('customer',)
    list_filter = ('customer',)

    def get_related_objects(self, obj):
        return ', '.join([item.name for item in obj.products.all()])

    get_related_objects.short_description = "Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    search_fields = ('cart__customer', 'product__name')
    list_filter = ('cart__customer', 'product__name')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'contact_email', 'contact_phone', 'is_active')
    search_fields = ('name', 'contact_email', 'is_active')
    list_filter = ('name',)

admin.site.register(Supplier, SupplierAdmin)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'product__name',
                    'order',
                    'quantity',
                    'total_price',
                    'created_at',
                    'updated_at']
    search_fields = ('product__name',)
    list_filter = ('product__name', 'created_at',)
    ordering = ('-created_at',)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',
                'customer',
                'order_date',
                'complete',
                'received_date',
                'status',
                'created_at',)
    search_fields = ['customer', 'complete']
    list_filter = ('created_at',)
    ordering = ('-order_date',)


class ProductLocationAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'address')
    search_fields = ('name', 'address')

admin.site.register(ProductLocation, ProductLocationAdmin)


class ExpiryTrackingAdmin(admin.ModelAdmin):
    list_display = ('id','item', 'expiration_date')
    search_fields = ('item__name', 'expiration_date',)
    list_filter = ('expiration_date',)



admin.site.register(ExpiryTracking, ExpiryTrackingAdmin)

@admin.register(ProductStockAdjustment)
class ProductStockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'item', 'quantity','location', 'transaction_date')
    search_fields = ('item__name', 'transaction_type', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')
    ordering = ('-transaction_date',)