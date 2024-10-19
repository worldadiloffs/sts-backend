
from modeltranslation.translator import TranslationOptions,register
from .models import SubCategory , MainCategory , SuperCategory 

@register(SubCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('sub_name', 'sub_meta', 'sub_content', 'seo_cub', )


@register(MainCategory)
class MainCategoryTranslationOptions(TranslationOptions):
    fields = ('main_name', 'main_meta', 'main_content')


@register(SuperCategory)
class SuperCategoryTranslationOptions(TranslationOptions):
    fields = ('super_name', 'meta_name', 'meta_content', 'seo_content', 'super_image_content',)




