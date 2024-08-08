from django.db import models
from category.models import SubCategory, SuperCategory, MainCategory
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import random, string
from PIL import Image as image
from django.utils.html import format_html
from datetime import date 
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime 
from django.http import JsonResponse 

import requests

class Testimage(models.Model):
    images = models.FileField(upload_to='files', blank=True, null=True)


class Image(models.Model):
    product = models.ForeignKey(
        "product.Product", models.SET_NULL, null=True, related_name="images"
    )
    image = models.ImageField(upload_to="products", blank=False, null=True)

class Product(models.Model):
    """ product models integration crm """
    product_name = models.CharField(max_length=300, blank=True)
    
    material_nomer = models.BigIntegerField(blank=True, null=True, unique=True, editable=False)
    
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    
    articul = models.PositiveIntegerField(blank=True , null=True)
    
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    
    meta_data = models.CharField(max_length=300, blank=True, null=True)
    
    tavar_dagavornaya = models.BooleanField(default=False,)
    
    super_category = models.ForeignKey(SuperCategory, on_delete=models.SET_NULL,  blank=True, null=True)
    
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL,  blank=True,  null=True)
    
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL,  blank=True, null=True)
    
    product_status = models.BooleanField(default=False, blank=True)
    
    # short_description = RichTextField(blank=True, null=True)

    short_content = models.JSONField(blank=True, null=True)
    
    content = models.JSONField(blank=True, null=True)
    
    full_description = RichTextField(blank=True, null=True)
    
    product_video = models.FileField(upload_to="productvideo", blank=True, null=True,)
    
    product_picture = models.ImageField(upload_to="products/images/", verbose_name="product images", blank=True, null=True)
    
    deliver_date = models.PositiveIntegerField(blank=True, null=True)
    
    price = models.PositiveIntegerField(blank=True, null=True)
    
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    
    # create_date = models.DateTimeField(auto_now_add=True, blank=True , editable=False)
    
    site_sts = models.BooleanField(default=False, blank=True)
    
    site_rts = models.BooleanField(default=False, blank=True)
    
    serenaTrue_countFalse = models.BooleanField(default=True, editable=False)

    counts = models.IntegerField(blank=True, default=0) 

    max_count = models.IntegerField(blank=True, default=0)

    xitlar = models.BooleanField(default=False, blank=True)
    # filter product news
    news = models.BooleanField(default=False, blank=True)
    # banner product add filter 
    banner_add = models.BooleanField(default=False, blank=True)
    #  aksiya product 
    aksiya = models.BooleanField(default=False, blank=True)

    news_title = models.CharField(max_length=20, blank=True, null=True)

    aksiya_title = models.CharField(max_length=20, blank=True, null=True)

    xitlar_title = models.CharField(max_length=50, blank=True, null=True)
    
    status = models.BooleanField(default=False, blank=True)
    

    
    
    @property
    def image(self):
        obj = self.images.first()
        if obj and obj.image:
            return obj.image.url
        return None
    def image_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image))
    @property
    def image_count(self):
        return self.images.all().count()

    @property
    def url(self):
        return reverse("products_detail", kwargs={"slug": self.slug})

    @property
    def has_banner_ad(self):
        if self.banner_ad:
            return True
        return False


    class Meta:
        verbose_name_plural = "Product"
        ordering = ["pk", "product_name"]

    def __str__(self):
        return self.product_name


    @classmethod
    def make_slug(cls,product_name):
        slug = slugify( product_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                product_name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.title() if self.product_name else self.product_name
        self.slug = self.make_slug(self.product_name)
        if self.main_category is not None:
            if not (MainCategory.objects.filter(id=self.main_category.pk).first().superCategory.pk == self.super_category.pk):
                raise  ValueError({"data": "errors"})
        if self.sub_category is not None:
            if not (SubCategory.objects.filter(id=self.sub_category.pk).first().mainCategory.pk == self.main_category.pk):
                raise  ValueError({"data": "errors"})
        if self.sub_category is not None:
            self.short_content_ru = self.sub_category.product_content_ru
            self.short_content_uz = self.sub_category.product_content_uz
        super().save(*args, **kwargs)




class FiltersProduct(models.Model):
    subcategory = models.OneToOneField(SubCategory, on_delete=models.SET_NULL, blank=True, null=True)
    product_filter = models.JSONField(blank=True)
    data_create = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)

    
