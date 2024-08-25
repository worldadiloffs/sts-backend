from django.contrib import admin
from .models import SubCategory , MainCategory , SuperCategory
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin

from product.models import Product
# Register your models here.

@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(sts_site=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(rts_site=True)
        else:
            qs = super().get_queryset(request)
            return qs.filter()
    list_display = ("sub_name",  "sts_site", "rts_site","image_tag")
    readonly_fields = ("sub_meta","seo_cub",)
    list_editable = ( "sts_site", "rts_site",)
    list_filter = ( "sts_site", "rts_site",)
    search_fields = ("sub_name","id",)
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    group_fieldsets = False 
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(MainCategory)
class MainCategoryAdmin(TranslationAdmin):
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(sts_site=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(rts_site=True)
        else:
            qs = super().get_queryset(request)
            return qs.filter()
            return qs.filter(sts_site=True)
    list_display = ("main_name", 'sts_site', 'rts_site', 'header_add', 'ommabob', 'status',"image_tag",)
    list_editable = ("status", "header_add", "ommabob","sts_site", "rts_site",)
    search_fields = ("main_name","id",)
    list_filter=('sts_site', 'rts_site', 'status',)
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    group_fieldsets = False 
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }



@admin.register(SuperCategory)
class SuperCategoryAdmin(TranslationAdmin):
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(sts_site=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(rts_site=True)
        else:
            qs = super().get_queryset(request)
            return qs.filter()
    list_display = ("super_name", "status", "sts_site", "rts_site", "image_tag",)
    list_editable = ("status", "sts_site", "rts_site",)
    search_fields = ("super_name","id", )
    list_filter=('sts_site', 'rts_site', 'status',)
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    group_fieldsets = False 
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }