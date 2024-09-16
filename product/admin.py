from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.db.models.fields.json import JSONField
from product.models import Image, Product 
# admin.site.register(Testimage)
from category.models import MainCategory , SuperCategory , SubCategory

@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('display_image_admin', 'product', 'title', 'cloudflare_id',)


class GalleryInlines(admin.TabularInline):
    model = Image
    max_num = 6


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    # class Media:
    #     js = ('admin/js/custom_admin.js',)


# @admin.register(Product)
class ProductsModelAdmin(TranslationAdmin): 
    form = ProductAdminForm
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
                kwargs["queryset"] = MainCategory.objects.filter()
            if db_field.name == "super_category":
                kwargs["queryset"] = SuperCategory.objects.filter(sts_site=True)
            if db_field.name == "sub_category":
               # Tanlangan asosiy modelga qarab querysetni filtrlash
                parent_instance = getattr(request, 'main_category', None)
                if parent_instance:
                    kwargs['queryset'] = SubCategory.objects.filter(mainCategory=parent_instance)
                else:
                    kwargs['queryset'] = SubCategory.objects.filter(sts_site=True)  # Agar tanlanmagan bo'lsa, hech narsa ko'rsatmaymiz
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
    
    list_max_show_all = 10
    list_per_page = 10
    # ordering = ("-id",)

    search_help_text="product nomi category nomi orqali qidirish"
    ordering = ('-id',)
    list_display = [
        "articul",
        "product_name",
        "counts",
        "category_obj",
        "price",
        "image_tag",
        "get_images",
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
        "short_description",
        "full_description", 
        # "short_content",
        # "content",
        "xitlar",
        "news",
        "banner_add",
        "aksiya",
        "price",
        "site_sts",
        "site_rts",
        "counts",
    ]

    inlines = [GalleryInlines]

    search_fields = [
        "product_name",
        "articul",
        "super_category__super_name",
        "main_category__main_name",
        "sub_category__sub_name",
    ]
    list_editable = [
        "counts",
        "price",
        # "site_sts",
        # "site_rts",
        "status",
    ]
    list_filter = [
        # "site_sts",
        # "site_rts",
        "status",
        "super_category__super_name",
        "main_category__main_name",
        "sub_category__sub_name",
    ]
    group_fieldsets = True 
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
            'admin/js/custom_admin.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    def get_form(self, request, obj=None, **kwargs):
        # Tanlangan asosiy model instanceini olish
        request.main_category = obj.main_category if obj else None
        return super().get_form(request, obj, **kwargs)


admin.site.register(Product, ProductsModelAdmin)