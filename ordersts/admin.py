from collections import OrderedDict
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import SafeText
from .models import Order, OrderItem , VazvratProdcut
# Register your models here.
from account.models import User
from django.utils.html import format_html

from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse

admin.site.register(VazvratProdcut)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # readonly_fields =("serena",)
    list_display = (
        'id','zakas_id', 'product', 'quantity', 'created_at', 'updated_at', 'user',
    )


class OrderAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__phone', 'yetkazish', 'zakas_id',)
    list_filter = ('status', 'yetkazish', 'created_at', 'updated_at',)
    change_list_template = 'admin/orders/order/change_list.html'
    readonly_fields = ( "total_price", 'created_at', 'updated_at', 'order_items', 'cashback', 'depozit','user',"site_sts", "site_rts","vazvrat_product", )
    list_editable = ('comment',  'status',)
    list_display = ( 'get_status','id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'comment', 'is_finished', 'get_product_names',)

    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(site_sts=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(site_rts=True)
        else:
            qs = super().get_queryset(request)
            return qs.filter()
        
    def get_status(self, obj):
        if obj.status == 'pending':
            print(obj.status)
            color = 'red'
        else:
            color = 'green'
        
        # return f'<span style="color: {color};">{obj.get_status_display()}</span>'
        return format_html('<span style="color: {};">{}</span>', color, obj.status)
    get_status.short_description = 'Status'
    def save_model(self, request, obj, form, change):
        # if not obj.pk:  # If the object is being created (not updated)
        #     obj.created_by = request.user
        # obj.modified_by =f"{request.user.phone}"  # Track who last modified it
        super().save_model(request, obj, form, change)


admin.site.register(Order, OrderAdmin)