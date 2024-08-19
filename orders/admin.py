from django.contrib import admin
from .models import Order, OrderItem 
# Register your models here.



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'quantity', 'price', 'created_at', 'updated_at', 'user',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_editable = ('comment', 'is_finished')
    list_display = (
        'id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'comment', 'is_finished', 'get_product_names',
    )