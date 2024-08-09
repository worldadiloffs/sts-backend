
from modeltranslation.translator import TranslationOptions,register
from .models import BlogCategory , BlogHome , BlogItem , Tag

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title', 'url')



@register(BlogHome)
class BlogHOmeTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

@register(BlogItem)
class BlogItemTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(BlogCategory)
class BlogCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
