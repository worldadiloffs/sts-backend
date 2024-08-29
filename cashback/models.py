from django.db import models

from account.models import User
# Create your models here.
class CashbackKard(models.Model):
    card = models.PositiveBigIntegerField(blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)
    balance = models.PositiveIntegerField(default=0, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)
    is_locked = models.BooleanField(default=False, blank=True)
    hisobot =models.JSONField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)
    site_sts = models.BooleanField(default=True, blank=True)
    site_rts = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return str(self.card)
    class Meta:
        verbose_name_plural = 'Cashback Kardlar' 
        ordering = ['id']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        