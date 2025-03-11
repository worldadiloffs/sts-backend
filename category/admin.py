from django.contrib import admin
from .models import SubCategory , MainCategory , SuperCategory
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin

from product.models import Product
# Register your models here.

@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    def save_model(self, request, obj, form, change):
        user = request.user
        # Custom logic before saving the object
        if not change:  # If the object is being created (not edited)
            if user.site_sts:
                obj.sts_site = True
            if user.site_rts:
                obj.rts_site = True
        # Save the object
        super().save_model(request, obj, form, change)


    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if db_field.name == "mainCategory":
            if user.site_sts:
                kwargs["queryset"] = MainCategory.objects.filter(sts_site=True)
            if user.site_rts:
                kwargs["queryset"] = MainCategory.objects.filter(rts_site=True)
            if not(user.site_sts) and not(user.site_rts):
                kwargs["queryset"] = MainCategory.objects.filter(sts_site=True, rts_site=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
    list_editable = ( "sts_site", "rts_site",)
    readonly_fields = ("product_description","product_content",)
    list_display = ("sub_name",  "sts_site", "rts_site","image_tag")
    readonly_fields = ("sts_site", "rts_site",)
    # list_editable = ( "sts_site", "rts_site",)
    list_filter = ( "sts_site", "rts_site",)
    search_fields = ("sub_name","id",)
    ordering = ("-id",)
    list_max_show_all = 10
    list_per_page = 10

    fields = [
        "rating",
        "mainCategory",
        "sub_name",
        "sub_image",
        "cloudflare_id",
        "sub_content",
        "sub_meta",
        "seo_cub"
    ]
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
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if db_field.name == "superCategory":
            if user.site_sts:
                kwargs["queryset"] = SuperCategory.objects.filter(sts_site=True)
            if user.site_rts:
                kwargs["queryset"] = SuperCategory.objects.filter(rts_site=True)
            if not(user.site_sts) and not(user.site_rts):
                kwargs["queryset"] = SuperCategory.objects.filter(sts_site=True, rts_site=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        user = request.user
        # Custom logic before saving the object
        if not change:  # If the object is being created (not edited)
            if user.site_sts:
                obj.sts_site = True
            if user.site_rts:
                obj.rts_site = True
        # Save the object
        super().save_model(request, obj, form, change)
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
    # readonly_fields = ("sts_site", "rts_site",)
    list_display = ("main_name", 'sts_site', 'rts_site', 'header_add', 'ommabob', 'status',"image_tag",)
    list_editable = ("status", "header_add", "ommabob", 'sts_site', 'rts_site',)
    search_fields = ("main_name","id",)
    list_filter=('sts_site', 'rts_site', 'status',)
    fields = ["rating", "superCategory", "main_name", "main_image", "icon","header_add", "ommabob", "status","cloudflare_id", "main_meta", "main_content"]
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
    def save_model(self, request, obj, form, change):
        user = request.user
        # Custom logic before saving the object
        if not change:  # If the object is being created (not edited)
            if user.site_sts:
                obj.sts_site = True
            if user.site_rts:
                obj.rts_site = True
        # Save the object
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(sts_site=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(rts_site=True)
    # readonly_fields = ("sts_site", "rts_site",)
    list_display = ("super_name", "status", "sts_site", "rts_site", "image_tag",)
    list_editable = ("status","sts_site", "rts_site",)
    search_fields = ("super_name","id", )
    list_filter=('sts_site', 'rts_site', 'status',)
    fields = ["rating","super_name", "category_image", "super_image_content", "icon", "status","cloudflare_id","meta_name","meta_content", "seo_content",]
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