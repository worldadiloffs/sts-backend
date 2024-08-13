from django.utils.text import slugify
import random
import string


from django.conf import settings


SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)


def code_generator(size=5, chars=string.ascii_lowercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))


def create_shortcode_super(instance):
    #new_slug = code_generator(size=size)
    new_slug = f"{slugify(instance.super_name,allow_unicode=True)}-{code_generator()}"
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slug).exists()
    if qs_exists:
        return create_shortcode_super(instance)
    return new_slug


def create_shortcode_main(instance):
    #new_slug = code_generator(size=size)
    new_slug = f"{slugify(instance.main_name,allow_unicode=True)}-{code_generator()}"
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slug).exists()
    if qs_exists:
        return create_shortcode_main(instance)
    return new_slug

def create_shortcode_sub(instance):
    #new_slug = code_generator(size=size)
    new_slug = f"{slugify(instance.sub_name,allow_unicode=True)}-{code_generator()}"
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slug).exists()
    if qs_exists:
        return create_shortcode_sub(instance)
    return new_slug