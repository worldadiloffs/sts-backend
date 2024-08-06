
from modeltranslation.translator import TranslationOptions,register
from .models import Banner , HomePageCategory 

@register(Banner)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'image',)

@register(HomePageCategory)
class HomePageCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)