# inventory/admin.py

from datetime import datetime
from django.contrib import admin
from .models import Category, InventoryItem, InventoryTransaction,InventoryLocation,ExpiryTracking, Order

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'quantity', 'reorder_level', 'location')
    search_fields = ('name', 'supplier__name', 'category__name')
    list_filter = ('category', 'supplier', 'location')
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)

# suppliers/admin.py

from django.contrib import admin
from .models import Supplier

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'is_active')
    search_fields = ('name', 'contact_email', 'is_active')
    list_filter = ('name',)

admin.site.register(Supplier, SupplierAdmin)

# orders/admin.py

from django.contrib import admin
from .models import OrderItem

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','supplier', 'inventory_item', 'quantity', 'order_date', 'received_date')
    search_fields = ('supplier__name', 'item__name')
    list_filter = ('supplier', 'received_date', 'order_date')
    ordering = ('-order_date',)

admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',
                'get_related_objects',
                'product_record',
                'ordered',
                'ordered_date',
                'created_at',
                'updated_at')
    search_fields = ['get_related_objects']
    list_filter = ('ordered_date',)
    ordering = ('-ordered_date',)

    def get_related_objects(self, obj):
        return ', '.join([item.inventory_item.name for item in obj.items.all()])

    get_related_objects.short_description = "Items"


admin.site.register(Order, OrderAdmin)




class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

admin.site.register(InventoryLocation, InventoryLocationAdmin)


class ExpiryTrackingAdmin(admin.ModelAdmin):
    list_display = ('item', 'expiration_date')
    search_fields = ('item__name', 'expiration_date',)
    list_filter = ('expiration_date',)



admin.site.register(ExpiryTracking, ExpiryTrackingAdmin)


class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'item', 'quantity', 'transaction_date')
    search_fields = ('item__name', 'transaction_type', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')
    ordering = ('-transaction_date',)

admin.site.register(InventoryTransaction, InventoryTransactionAdmin)