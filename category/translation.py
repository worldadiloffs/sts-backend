
from modeltranslation.translator import TranslationOptions,register
from .models import SubCategory , MainCategory , SuperCategory , SuperCategoryContent

@register(SubCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_content', 'sub_name', 'sub_meta', 'sub_content', 'seo_cub', 'product_description', 'product_content', 'product_filter')


@register(MainCategory)
class MainCategoryTranslationOptions(TranslationOptions):
    fields = ('main_name', 'main_meta', 'main_content')


@register(SuperCategory)
class SuperCategoryTranslationOptions(TranslationOptions):
    fields = ('super_name', 'meta_name', 'meta_content', 'seo_content')



@register(SuperCategoryContent)
class SuperCategoryContentTranslationOptions(TranslationOptions):
    fields = ('title', 'text', 'header_contet')



