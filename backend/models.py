from django.db import models

# Create your models here.
from account.models import User


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
