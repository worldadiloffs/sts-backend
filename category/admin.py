from django.contrib import admin
from .models import SubCategory , MainCategory , SuperCategory
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin
# Register your models here.

# admin.site.register(SuperCategory)
# admin.site.register(MainCategory)
# admin.site.register(SubCategory)


@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ("sub_name", "status", "sts_site", "rts_site")
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
    list_display = ("main_name", "status", "sts_site", "rts_site")
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
    list_display = ("super_name", "status", "site_sts", "site_sts")
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