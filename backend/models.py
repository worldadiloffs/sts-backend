from django.db import models

# Create your models here.
from account.models import User
from django.core.cache import cache


class Sites(models.Model):
    STATUS_CHOICES = (
        ('sts', "site sts"),
        ('rts', 'site rts'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sts')
    user_id = models.IntegerField(blank=True, unique=True, editable=False)


    def save(self, *args, **kwargs):
        if self.status == 'rts':
            user = User.objects.get(id=self.user_id)
            user.site_rts = True
            user.site_sts = False
            user.save()
        if self.status == 'sts':
            user = User.objects.get(id=self.user_id)
            user.site_sts = True
            user.site_rts = False
            user.save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.status} site'
    


class CaCheClear(models.Model):
    clear_cache = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.clear_cache:
            cache.clear()
            self.clear_cache = False
        super().save(*args, **kwargs)

