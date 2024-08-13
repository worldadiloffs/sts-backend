from django.contrib import admin
from .models import AboutPage, Banner , homePage , HomePageCategory
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin
# Register your models here.

# admin.site.register(SubCategory)


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
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
admin.site.register(AboutPage)

@admin.register(HomePageCategory)
class HomePageCategoryAdmin(TranslationAdmin):
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