from django.contrib import admin
from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor

# Register your models here.
from .models import CashbackKard




@admin.register(CashbackKard)
class CashbackKardAdmin(admin.ModelAdmin):
    readonly_fields = ('card','balance', 'get_user', 'site_sts', 'site_rts',)
    list_display = ('id','card','balance', 'get_user', 'site_sts', 'site_rts',)


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