from django.db import models

from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import Group
from account.models import User




class Xodim(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    marketing = models.BooleanField(default=False, blank=True)
    sotuvchi = models.BooleanField(default=False, blank=True)
    content_manager = models.BooleanField(default=False, blank=True)
    coll_center = models.BooleanField(default=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    permision = models.ManyToManyField(Group, blank=True)
    ishni_boshlash_vaqti = models.TimeField(blank=True, null=True)
    ishni_bitirish_vaqti = models.TimeField(blank=True, null=True)



    def get_permission_names(self):
        return ', '.join([p.name for p in self.permision.all()])
    
    
    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"

    def __str__(self):
        return self.user.phone + " - " + self.name
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)