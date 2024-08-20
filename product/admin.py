from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from product.models import Image, Product 
# admin.site.register(Testimage)
from category.models import MainCategory , SuperCategory , SubCategory

admin.site.register(Image)

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if  self.fields['main_category'].queryset is not None:
            self.fields['main_category'].queryset = MainCategory.objects.filter(superCategory=self.instance.super_category).order_by('id')







class AdminCreateFormMixin:
    """
    Mixin to easily use a different form for the create case (in comparison to "edit") in the django admin
    Logic copied from `django.contrib.auth.admin.UserAdmin`
    """
    add_form = None

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
    

class GalleryInlines(admin.TabularInline):
    model = Image
    max_num = 6



@admin.register(Product)
class ProductsModelAdmin(TranslationAdmin): 
    readonly_fields = ('full_description',)
    # add_form = ProductEditForm
    change_list_template = "admin/product/product/change-list.html"

     
    # def get_fields(self, request, obj=None):
    #     user = request.user
    #     # if user.is_authenticated:
    #     #     return super().get_fields(request, obj)
    #     fields = ["product_name", "articul", "price",]
    #     return fields
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "main_category":
            kwargs["queryset"] = MainCategory.objects.filter(sts_site=True)
        if db_field.name == "super_category":
            kwargs["queryset"] = SuperCategory.objects.filter(sts_site=True)
        if db_field.name == "sub_category":
            kwargs["queryset"] = SubCategory.objects.filter(sts_site=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(site_sts=True)
        else:
            qs = super().get_queryset(request)
            return qs.filter(site_rts=True)
    
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
        "site_rts"
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

    

