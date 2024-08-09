from modeltranslation.translator import TranslationOptions , register
from .models import CardGril , PageContent  , SitePage

@register(CardGril)
class CardGrilTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(PageContent)
class PageContentTranslationOptions(TranslationOptions):
    fields = ('title', 'content')





@register(SitePage)
class SitePageTranslations(TranslationOptions):
    fields = ('page_name',)
