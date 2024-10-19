from django.db import models
from category.models import SubCategory, SuperCategory, MainCategory
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import random, string
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from product.servisses import get_image_url_from_cloudflare, upload_image_to_cloudflare


from .utils import  create_shortcode 

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    cloudflare_id = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(
        "product.Product", models.SET_NULL, null=True, related_name="images"
    )
    image = models.ImageField(upload_to="products", blank=False, null=True)
    def save(self, *args, **kwargs):
        # Modelni oldindan saqlab qo'yamiz
        # super().save(*args, **kwargs)
        # if not self.cloudflare_id and self.image is not None:
        #     cload_id = upload_image_to_cloudflare(self.image.file)
        #     self.cloudflare_id = cload_id
        super().save(*args, **kwargs)



    @property
    def get_mobile(self):
        if not self.cloudflare_id:
            return None
        cloudflare_id = self.cloudflare_id
        img_url = get_image_url_from_cloudflare(cloudflare_id, variant="mobile")
        return img_url
    

    @property
    def get_admin_image(self):
        if not self.cloudflare_id:
            return ""
        cloudflare_id = self.cloudflare_id
        img_url = get_image_url_from_cloudflare(cloudflare_id, variant="admin")
        return img_url

    

    def display_image_admin(self):
        if not self.cloudflare_id:
            return ""
        cloudflare_id = self.cloudflare_id
        img_url = get_image_url_from_cloudflare(cloudflare_id, variant="admin")
        img_html = f'<img src="{img_url}">'
        return format_html(img_html)
    


class Product(models.Model):
    """ product models integration crm """
    product_name = models.CharField( max_length=500, blank=True)
    
    material_nomer = models.BigIntegerField(blank=True, null=True, unique=True, editable=False)
    
    slug = models.SlugField(unique=True, null=True, allow_unicode=True, editable=False, blank=True , max_length=400)
    
    articul = models.PositiveIntegerField(blank=True , null=True, unique=True)
    
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    
    meta_data = models.CharField(max_length=300, blank=True, null=True)
    
    tavar_dagavornaya = models.BooleanField(default=False,)
    
    super_category = models.ForeignKey(SuperCategory, on_delete=models.SET_NULL,  blank=True, null=True)
    
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL,  blank=True,  null=True)
    
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL,  blank=True, null=True)
    
    # product_status = models.BooleanField(default=False, blank=True)
    
    short_description = RichTextField(blank=True, null=True)

    short_content = models.JSONField(blank=True, null=True)
    
    content = models.JSONField(blank=True, null=True)
    
    full_description = RichTextField(blank=True, null=True)
    
    product_video = models.FileField(upload_to="productvideo", blank=True, null=True,)
    
    deliver_date = models.PositiveIntegerField(blank=True, null=True)
    
    price = models.FloatField(blank=True, null=True)
    
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
    
    available = models.BooleanField(default=True, blank=True, editable=False)


    def cart_title(self, obj):
        if self.news:
            return self.news_title
        


    def get_available(self):
        return f"{self.available}"
    
    def link(self):
        if self.sub_category is not None:
             return  {
                 
                    "super": {

                    "name": self.super_category.super_name,
                    "slug": self.super_category.slug,
                    },
                    "main": {
                        "name": self.main_category.main_name,
                        "slug": self.main_category.slug,
                    },
                    "sub": {
                      
                            "name": self.sub_category.sub_name,
                            "slug": self.sub_category.slug,
                    }
                   },
        if self.main_category is not None:
            return  {
             
                       "super": {
                   
                    "name": self.super_category.super_name,
                    "slug": self.super_category.slug,
                    },
                    "main": {
                        "name": self.main_category.main_name,
                        "slug": self.main_category.slug,
                    },
                   },
        if self.super_category:
            return  {
             
                       "super": {
                   
                    "name": self.super_category.super_name,
                    "slug": self.super_category.slug,
                    },
                   },
    
    
    @property
    def image(self):
        obj = self.images.first()
        if obj and obj.image:
            return obj.image.url
        return None
    
    def get_images(self):
        obj =  self.images.first()
        if obj:
            url = obj.get_admin_image
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(url))
        return ""

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
        if self.banner_add:
            return True
        return False


    class Meta:
        verbose_name_plural = "Tavarlar"
        ordering = ["pk", "product_name"]
        indexes = [
            models.Index(fields=['super_category', 'main_category', 'sub_category', 'articul', 'slug']),  # Yangi kompozit indeks
        ]

    def __str__(self):
        return self.product_name
     
    def category_obj(self):
        if self.super_category is not None:
            return f"{self.super_category.super_name}"
        return ""


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
        if not(self.site_sts) and not(self.site_rts):
            raise  ValueError({"data": "errors"})
        if self.main_category is not None:
            if not (MainCategory.objects.filter(id=self.main_category.pk).first().superCategory.pk == self.super_category.pk):
                raise  ValueError({"data": "errors"})
        if self.sub_category is not None:
            if not (SubCategory.objects.filter(id=self.sub_category.pk).first().mainCategory.pk == self.main_category.pk):
                raise  ValueError({"data": "errors"})
        if not self.slug or self.slug is None or self.slug == "":
            if self.product_name:
                self.product_name = self.product_name.strip()
            if not self.slug:
                product_name  = self.product_name[:50]
                self.slug = self.make_slug(product_name)
        super().save(*args, **kwargs)


