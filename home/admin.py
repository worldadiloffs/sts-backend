from django.contrib import admin
from .models import  Banner ,  HomePageCategory
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin
# Register your models here.

# admin.site.register(SubCategory)


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
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
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(site_sts=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(site_rts=True)
    list_display = ("title", "site_sts", "site_rts", "image_tag", "status",)
    list_editable = ("site_sts", "site_rts", "status",)
    search_fields = ("title",)
    list_filter = ("site_sts", "site_rts",)
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
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

@admin.register(HomePageCategory)
class HomePageCategoryAdmin(TranslationAdmin):
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
    def get_queryset(self, request):
        user = request.user
        if user.site_sts:
            qs = super().get_queryset(request)
            return qs.filter(site_sts=True)
        if user.site_rts:
            qs = super().get_queryset(request)
            return qs.filter(site_rts=True)
    list_display = ("top", "title", "category",  "status", "site_sts", "site_rts")
    list_editable = ("status","site_sts", "site_rts")
    search_fields = ("title",)
    list_filter = ("site_sts", "site_rts", "xitlar", "aksiya", "banner_add",)
    list_max_show_all = 10

    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
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