from django.contrib import admin
from .models import Banner , homePage , HomePageCategory
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

# @admin.register(homePage)
# class HOmePageAdmin(admin.ModelAdmin):
#     list_display = ('site_sts', 'site_rts',)
#     list_editable=  ("site_sts", "site_rts",)

#  status = models.BooleanField(default=False, blank=True) 
#     site_sts =models.BooleanField(default=False, blank=True)
#     site_rts =models.BooleanField(default=False, blank=True)
#       # filter product news
#     news = models.BooleanField(default=False, blank=True)
#     # banner product add filter 
#     banner_add = models.BooleanField(default=False, blank=True)
#     #  aksiya product 
#     aksiya = models.BooleanField(default=False, blank=True)
#     xitlar = models.BooleanField(default=False, blank=True)

@admin.register(HomePageCategory)
class HomePageCategoryAdmin(TranslationAdmin):
    list_display = ("top", "title", "category",  "image_tag", "site_sts", "site_rts")
    list_editable = ("status",)
    search_fields = ("title",)
    list_filter = ("site_sts", "site_rts", "xitlar", "aksiya", "banner_add",)

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