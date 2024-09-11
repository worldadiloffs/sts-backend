
from modeltranslation.translator import TranslationOptions,register
from .models import Product

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name','short_content', 'meta_title', 'meta_data', 'content','full_description', 'news_title', 'aksiya_title', 'short_description',)
