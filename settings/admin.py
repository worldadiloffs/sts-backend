from django.contrib import admin
from .models import (CardGril , PageContent  , PaymentMethod , DeliveryService, Shaharlar ,
                      SiteSettings , PaymentMethod , OrderSetting  , SitePage , SocialNetwork , 
                      CountSettings, Tumanlar, TolovUsullar, Dokon, MuddatliTolovxizmatlar, CashBackSetting, ServisPage)
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor
from modeltranslation.admin import TranslationAdmin
# Register your models here.
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor

@admin.register(ServisPage)
class ServisPageAdmin(TranslationAdmin):
    list_display = ("title",  "status", "site_sts", "site_rts",)
    search_fields = ("title",)

    


admin.site.register(Tumanlar)


@admin.register(Shaharlar)
class ShaharlarAdmin(admin.ModelAdmin):
    list_display = ("id","name",  "zakas_summa", "summa", "site_sts", "site_rts")
    search_fields = ("name",)
    list_filter = ("site_sts", "site_rts",)
    list_editable = ("zakas_summa", "summa", "site_sts", "site_rts",)



@admin.register(CashBackSetting)
class CashBackSettingAdmin(admin.ModelAdmin):
    list_display = ( "id","category_tavar", "product", "cashback_foiz", "status", "site_sts", "site_rts",)
    search_fields = ("category_tavar__name", "product__name",)
    list_filter = ("site_sts", "site_rts",)

@admin.register(Dokon)
class DokonAdmin(admin.ModelAdmin):
    list_display = ("name", "site_sts", "site_rts",)
    list_filter = ("site_sts", "site_rts",)
    search_fields = ("name",)



@admin.register(TolovUsullar)
class TolovUsullarAdmin(TranslationAdmin):
    list_display = ("id","name", "site_sts", "site_rts", "status",)
    list_filter = ("site_sts", "site_rts", "status",)
    search_fields = ("name",)



@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display =( "id","name", "image_tag", "status", "site_sts", "site_rts")
    list_editable = ("site_sts", "site_rts")
    search_fields = ("name",)


@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ("id","zakas_summa", "dastafka_summa", "site_sts", "site_rts",)




@admin.register(OrderSetting)
class OrderSettingAdmin(admin.ModelAdmin):
    list_display =("id","nds", "doller", "site_sts", "site_rts",)
    # list_editable = (  "nds", "site_sts", "site_rts",)
    list_filter= ( "site_sts", "site_rts",)



@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ("id","name",  "site_sts", "site_rts", "status",)
    search_fields = ("name",)
    list_filter = ("site_sts", "site_rts", "status",)





@admin.register(MuddatliTolovxizmatlar)
class MuddatliTolovxizmatlarAdmin(admin.ModelAdmin):
    list_display =("id","name",)

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