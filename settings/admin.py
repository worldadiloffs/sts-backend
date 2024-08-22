from django.contrib import admin
from .models import (CardGril , PageContent  , PaymentMethod , DeliveryService, Shaharlar ,
                      SiteSettings , PaymentMethod , OrderSetting  , SitePage , SocialNetwork , CountSettings, Tumanlar)
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin
# Register your models here.

admin.site.register(PaymentMethod)
admin.site.register(DeliveryService)
admin.site.register(OrderSetting)
admin.site.register(SocialNetwork)
admin.site.register(Shaharlar)
admin.site.register(Tumanlar)

@admin.register(CountSettings)
class CountSettingAdmin(admin.ModelAdmin):
    list_display = ("main_obj","count",)



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'image_tag')



@admin.register(CardGril)
class CartGrilAdmin(TranslationAdmin):
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

@admin.register(PageContent)
class PageContentAdmin(TranslationAdmin):
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

@admin.register(SitePage)
class PageTranslationAdmin(TranslationAdmin):
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


