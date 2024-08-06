from django.contrib import admin
from .models import Banner , homePage , HomePageCategory
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin
# Register your models here.

# admin.site.register(SubCategory)


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
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

@admin.register(homePage)
class HOmePageAdmin(admin.ModelAdmin):
      list_display = ('site_sts', 'site_rts',)


@admin.register(HomePageCategory)
class HomePageCategoryAdmin(TranslationAdmin):
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