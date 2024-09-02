
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from settings.models import OrderSetting
from django.core.cache import cache

@receiver(post_save, sender=OrderSetting)
def clear_cache_on_save(sender, instance, **kwargs):
    print("dsdsd")
    cache.delete('doller')  # Cache'dagi 'all_posts' ni o'chirish

# Cache ni yangilash uchun signal
@receiver(post_delete, sender=OrderSetting)
def clear_cache_on_delete(sender, instance, **kwargs):
    print("dsdsd")
    cache.delete('doller')  # Cache'dagi 'all_posts' ni o'chirish
