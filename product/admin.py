from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.db import models
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from account.models import User
from product.models import Image, Product , Testimage , FiltersProduct
# admin.site.register(Testimage)
from category.models import MainCategory , SubCategory
from django.contrib.auth.admin import UserAdmin 

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("hello words", self.instance.price)

        self.fields['main_category'].queryset = MainCategory.objects.filter(superCategory=self.instance.super_category)

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
    


# Register your models here.


@admin.register(FiltersProduct)
class ProductsModelAdmins(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    list_display = [
       "status",
    ]

class GalleryInlines(admin.TabularInline):
    model = Image
    max_num = 6

# class ProductVideo(admin.TabularInline):
#     model = ProductVideo
#     fields = 1


@admin.register(Product)
class ProductsModelAdmin(TranslationAdmin): 
    # form = ProductEditForm
    # add_form = ProductEditForm
    
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    list_display = [
        "product_name",
        "price",
        "image_tag",
    ]

    # fields = [
    #     "product_name",
    #     # "price",
    #     # "discount_price",
    #     "meta_title",
    #     "meta_data",
    #     "super_category",
    #     "main_category",
    #     "sub_category",
    #     "product_status",
    #     "product_video",
    #     "product_picture",
    #     # "short_description",
    #     "full_description", 
    #     # "material_nomer",
    #     "short_content",
    # ]

    inlines = [GalleryInlines]

    search_fields = [
        "product_name",
        "price",
    ]
    # list_editable = [
    #     "price",
    # ]
    list_filter = [
        "site_sts",
        "site_rts",
    ]
    # formfield_overrides = {
    # JSONField: {'widget': JSONEditor},
    # }
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

    

