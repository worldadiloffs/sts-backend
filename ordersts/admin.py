from collections import OrderedDict
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import SafeText
from .models import Order, OrderItem , VazvratProdcut , Cupon , CategoryProduct , ContactForm
# Register your models here.
from account.models import User
from django.utils.html import format_html

from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('ism', 'telefon', 'created_at',)


admin.site.register(VazvratProdcut)

class CategoryProductAdmin(admin.TabularInline):
    model = CategoryProduct
    max_num = 10

@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('id','code',  'status', 'site_sts', 'site_rts',)
    list_filter = ('status', 'site_sts', 'site_rts',)
    search_fields = ('code',)
    inlines = [CategoryProductAdmin]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ('product__product_name', 'user__phone', 'zakas_id',)
    list_filter = ('created_at',)
    ordering = ('-zakas_id',)

    # readonly_fields =("serena",)
    list_display = (
        'id','zakas_id', 'product', 'quantity', 'created_at', 'updated_at', 'user',
    )
    list_max_show_all = 10
    list_per_page = 10


class OrderAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__phone', 'yetkazish', 'zakas_id',)
    list_filter = ('status', 'yetkazish', 'created_at', 'updated_at',)
    # change_list_template = 'admin/orders/order/change_list.html'
    readonly_fields = (  'created_at', 'updated_at', 'order_items', 'cashback', 'depozit','user',"site_sts", "site_rts","vazvrat_product", )
    list_editable = ('comment',  'status','is_finished')
    list_display = ( 'get_status','id', 'user', 'status', 'created_at', 'total_price', 'comment', 'is_finished', 'get_product_names',)

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

    list_max_show_all = 10
    list_per_page = 10
    def get_status(self, obj):
        if obj.status == 'pending':
            color = 'red'
        else:
            color = 'green'
        # return f'<span style="color: {color};">{obj.get_status_display()}</span>'
        return format_html('<span style="color: {};">{}</span>', color, obj.status)
    get_status.short_description = 'Status'

admin.site.register(Order, OrderAdmin)