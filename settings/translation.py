from modeltranslation.translator import TranslationOptions , register
from .models import CardGril , PageContent  , SitePage , Shaharlar, SiteSettings , Tumanlar , TolovUsullar 

@register(TolovUsullar)
class TolovUsullarTranslationOptions(TranslationOptions):
    fields = ('name', 'content')

@register(CardGril)
class CardGrilTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(PageContent)
class PageContentTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(SitePage)
class SitePageTranslations(TranslationOptions):
    fields = ('page_name',)



@register(Shaharlar)
class ShaharlarTranslationOptions(TranslationOptions):
    fields = ('name',)


# @register(SiteSettings)
# class SiteSettingsTranslationOptions(TranslationOptions):
#     fields = ('site_name', 'image_tag')

@register(Tumanlar)
class TumanlarTranslationOptions(TranslationOptions):
    fields = ('name',)
