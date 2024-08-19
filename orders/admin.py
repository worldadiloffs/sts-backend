from collections import OrderedDict
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import SafeText
from .models import Order, OrderItem , TestModelUser
# Register your models here.
from account.models import User


@admin.register(TestModelUser)
class TestModelUserAdmin(admin.ModelAdmin):
    def get_actions(self, request: HttpRequest, obj) -> OrderedDict[Any, Any]:
        user  = request.user
        print( "hello " ,obj)
        self.get_changelist_form(request)
        return super().get_actions(request)
    
    def get_empty_value_display(self) -> SafeText:
        print(self.get_action_choices())
        return super().get_empty_value_display()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields =("serena",)
    list_display = (
        'id', 'product', 'quantity', 'price', 'created_at', 'updated_at', 'user',
    )
    list_display = (
        'id', 'product', 'quantity', 'price', 'created_at', 'updated_at', 'user',
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ( "total_price",'is_finished', 'created_at', 'updated_at', 'order_items', 'cashback', 'depozit','user',"site_sts", "site_rts","vazvrat_product", )
    list_editable = ('comment',  'status',)
    list_display = (
        'id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'comment', 'is_finished', 'get_product_names',
    )