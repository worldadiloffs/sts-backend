from django.db import models
from ckeditor.fields import RichTextField 
from django.utils.text import slugify
import random, string

import random, string
from PIL import Image as image
from django.utils.html import format_html
from datetime import date 
from django.urls import reverse
# Create your models here.

from category.models import MainCategory

# Biz haqimizda , kafolat , aksiya Bizning dokonlarimiz
class CardGril(models.Model):
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='cards', blank=True, null=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title
    

class SitePage(models.Model):
    page_name = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)



    def __str__(self):
        return self.page_name


    
class PageContent(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='malumot/image', blank=True, null=True)
    content = RichTextField(blank=True)
    card = models.ManyToManyField(CardGril, blank=True) 
    date_create = models.DateField(auto_now_add=True, blank=True)
    pages = models.ForeignKey(SitePage , on_delete=models.SET_NULL , blank=True,  null=True)
    site_sts =models.BooleanField(default=False, blank=True)
    site_rts =models.BooleanField(default=False, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)


    class Meta:
        verbose_name_plural = "Page"
        ordering = ["pk", "title"]

    def __str__(self):
        return self.title


    @classmethod
    def make_slug(cls,  title):
        slug = slugify( title, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                 title + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug


    def save(self, *args, **kwargs):
        self.title = self.title.title() if self. title else self. title
        self.slug = self.make_slug(self.title)

        super().save(*args, **kwargs)

     
# Xizmatlar tolov usullari Ommaviy tolovlar Hamkorlik , ustanofka xizmat , Hamkorlik , qaytarish siyosati

#yetkazib berish . biz bilan bog'lanish , servis center , vakansiya


class DeliveryService(models.Model):
    comment = models.CharField(max_length=100, blank=True) 
    zakas_summa = models.BigIntegerField(blank=True)
    dastafka_summa = models.BigIntegerField(blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.zakas_summa} {self.dastafka_summa}"


class SocialNetwork(models.Model):
    name = models.CharField(max_length=50, blank=True)
    icon = models.FileField(upload_to='socialnetwork', blank=True)
    link = models.URLField(blank=True)
    status = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    site_data = models.CharField(max_length=5, blank=True, null=True, editable=False)


    def save(self, *args, **kwargs):
        if self.site_data is None:
            if self.site_sts:
                self.site_data = "sts"
            if self.site_rts:
                self.site_data = "rts"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} {self.site_data}"




class SiteSettings(models.Model):
    logo = models.ImageField(upload_to="logo/images", blank=True)
    icon = models.FileField(upload_to='logo/images', blank=True, null=True)
    site_name = models.CharField(max_length=50, blank=True, null=True)
    file_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    socialnetwork = models.ManyToManyField(SocialNetwork, blank=True)
    site_stopped = models.BooleanField(default=False, blank=True)
    open_time = models.CharField(max_length=30, blank=True, null=True)
    close_time = models.CharField(max_length=30, blank=True, null=True)
    date_week = models.CharField(max_length=50, blank=True, null=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    footer_logo = models.ImageField(upload_to='logo/image', blank=True, null=True)


    def image_tag(self):
        if self.logo is not None:
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.logo.url))
        else:
            return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='payment', blank=True)
    content = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)


    def __str__(self):
        return f"{self.name}"
    


class CountSettings(models.Model):
    mainCategory = models.OneToOneField(MainCategory, on_delete=models.SET_NULL, blank=True, null=True)
    count = models.IntegerField(default=5, blank=True)

    def main_obj(self):
        if self.mainCategory is not None:
            return f"{MainCategory.objects.get(id=self.mainCategory.pk).main_name}"



class OrderSetting(models.Model):
    depozit_tolov = models.BooleanField(default=False, blank=True)
    cashback_tolov = models.BooleanField(default=False, blank=True)
    tolov_online = models.BooleanField(default=True, blank=True)
    nds = models.PositiveIntegerField(blank=True, null=True)
    date_update =  models.DateField(blank=True, null=True)
    cource_valyuta = models.PositiveIntegerField(blank=True, null=True)
    tolov_usullar = models.ManyToManyField(PaymentMethod, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    doller = models.IntegerField(blank=True, null=True) 


    def __str__(self):
        return f"Depozit tolov: {self.depozit_tolov}, Cashback tolov: {self.cashback_tolov}, NDS: {self.nds}, Cource Valyuta: {self.cource_valyuta}, Tolov Online: {self.tolov_online}"