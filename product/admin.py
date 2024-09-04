from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from product.models import Image, Product 
# admin.site.register(Testimage)
from category.models import MainCategory , SuperCategory , SubCategory


class GalleryInlines(admin.TabularInline):
    model = Image
    max_num = 6



@admin.register(Product)
class ProductsModelAdmin(TranslationAdmin): 

    readonly_fields = ('site_sts', 'site_rts')
    def save_model(self, request, obj, form, change):
        user = request.user
        # Custom logic before saving the object
        if not change:  # If the object is being created (not edited)
            if user.site_sts:
                obj.site_sts = True
            if user.site_rts:
                obj.site_rts = True
        # Save the object
        super().save_model(request, obj, form, change)  

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if user.site_sts:
            if db_field.name == "main_category":
                kwargs["queryset"] = MainCategory.objects.filter(sts_site=True)
            if db_field.name == "super_category":
                kwargs["queryset"] = SuperCategory.objects.filter(sts_site=True)
            if db_field.name == "sub_category":
                kwargs["queryset"] = SubCategory.objects.filter(sts_site=True)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if user.site_rts:
            if db_field.name == "main_category":
                kwargs["queryset"] = MainCategory.objects.filter(rts_site=True)
            if db_field.name == "super_category":
                kwargs["queryset"] = SuperCategory.objects.filter(rts_site=True)
            if db_field.name == "sub_category":
                kwargs["queryset"] = SubCategory.objects.filter(rts_site=True)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(site_sts=True)
        elif user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(site_rts=True)
        else:
            qs = super().get_queryset(request)
            return qs.all()
    
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    
    list_max_show_all = 10
    list_per_page = 10

    search_help_text="product nomi category nomi orqali qidirish"
    ordering = ('-id',)
    list_display = [
        "articul",
        "product_name",
        "counts",
        "category_obj",
        "price",
        "image_tag",
        "site_sts",
        "site_rts",
        "status",
    ]

    fields = [
        "product_name",
        'articul',
        "super_category",
        "main_category",
        "sub_category",
        "product_video",
        "full_description", 
        "short_content",
        "content",
        "xitlar",
        "xitlar_title",
        "news",
        "news_title",
        "banner_add",
        "aksiya",
        "aksiya_title",
        "price",
        "site_sts",
        "site_rts",
        "counts",
    ]

    inlines = [GalleryInlines]

    search_fields = [
        "product_name",
        "price",
        "super_category__super_name",
        "main_category__main_name",
        "sub_category__sub_name",
    ]
    list_editable = [
        "counts",
        "site_sts",
        "site_rts",
        "status",
    ]
    list_filter = [
        "site_sts",
        "site_rts",
        "super_category__super_name",
        "main_category__main_name",
        "sub_category__sub_name",
    ]
    group_fieldsets = True 
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    

