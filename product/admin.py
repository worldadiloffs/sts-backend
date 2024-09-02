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
    actions = ["main_category_change"]

    # readonly_fields = ('full_description',)
    # add_form = ProductEditForm
    change_list_template = "admin/product/product/change-list.html"

    # autocomplete_fields = ("main_category", "super_category", "sub_category",)

    # def get_fields(self, request, obj=None):
    #     user = request.user
    #     # if user.is_authenticated:
    #     #     return super().get_fields(request, obj)
    #     fields = ["product_name", "articul", "price","full_description"]
    #     return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if user.site_sts:
            if db_field.name == "main_category":
                if request._obj_ is not None:
                # `request._obj_` uchun to'g'ri URL mavjud bo'lishi kerak
                    kwargs['queryset'] = MainCategory.objects.filter(superCategory=request._obj_.super_category, sts_site=True)
                else:
                    kwargs["queryset"] = MainCategory.objects.filter(sts_site=True)
                # kwargs["queryset"] = MainCategory.objects.filter(sts_site=True)
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
            return qs.filter(site_sts=False, site_rts=True)
    
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

    

