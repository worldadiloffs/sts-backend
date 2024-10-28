from django.db import models
from django.utils.translation import gettext_lazy as _
from category.models import MainCategory , SubCategory
from django.utils.text import slugify
import random, string
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
# Create your models here.
from config.settings import site_name 

from django.utils.html import format_html

from product.servisses import get_image_url_from_cloudflare, upload_image_to_cloudflare 

class Banner(models.Model):
    title = models.CharField(max_length=200, blank=True , verbose_name=_("Banner uchun nom"))
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Status"))
    url = models.URLField(blank=True, verbose_name=_("URL Linki"))
    image = models.ImageField(upload_to='banner/images', blank=True, verbose_name=_("Rasim"))
    category = models.ForeignKey(MainCategory , on_delete=models.SET_NULL , blank=True, null=True, verbose_name=_("Kategoriya"))
    cloudflare_id = models.CharField(max_length=200, blank=True, null=True)
    site_sts =models.BooleanField(default=False, blank=True, verbose_name=_("Site STS"))
    site_rts =models.BooleanField(default=False, blank=True, verbose_name=_("Site RTS"))
    
    class Meta:
        verbose_name_plural = "Home Banner"
        ordering = ["pk", "title"]
    

    def __str__(self):
        return self.title


    @classmethod
    def make_slug(cls, title):
        slug = slugify(title, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                title + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug
    
    def image_tag(self):
        if self.image is not None:
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image.url))
        else:
            return None
    


    def save(self, *args, **kwargs):
        self.title = self.title.title() if self.title else self.title
        self.slug = self.make_slug(self.title)
        super().save(*args, **kwargs)
        if not self.cloudflare_id and self.image is not None:
            cload_id = upload_image_to_cloudflare(self.image.file)
            self.cloudflare_id = cload_id
        super().save(*args, **kwargs)    


        # def save(self, *args, **kwargs):
        # Rasmni o'qish
        # if self.image:
        #     img = Image.open(self.image)

        #     # Agar format webp bo'lsa
        #     if img.format.lower() == 'webp':
        #         img = img.convert('RGB')  # webp ni jpg formatiga mos ravishda o'zgartirish

        #         # Faylni o'zgartirish
        #         img_io = BytesIO()
        #         img.save(img_io, format='JPEG')

        #         # Eski faylni yangi fayl bilan almashtirish
        #         new_image = File(img_io, name=self.image.name.replace('webp', 'jpg'))
        #         self.image.save(new_image.name, new_image, save=False)

        # super().save(*args, **kwargs)




class CardImage(models.Model):
    images = models.ImageField(upload_to='minicard/images', blank=True, null=True)
    cloudflare_id = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, verbose_name=_("status"))
    homepagecategory = models.ForeignKey(
        "home.HomePageCategory", models.SET_NULL, null=True, related_name="cardimage"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.cloudflare_id and self.images is not None:
            cload_id = upload_image_to_cloudflare(self.images.file)
            self.cloudflare_id = cload_id
        super().save(*args, **kwargs)


    def image_obj(self):
        if self.cloudflare_id:
            return get_image_url_from_cloudflare(self.cloudflare_id)
        
        else:
            if self.images:
                return site_name + self.images.url
            return None
   



class HomePageCategory(models.Model):
    top= models.IntegerField(blank=True, null=True, help_text=_("home page nechinchi orinda chiqsin"))
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Nom"))
    mainCategory = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, blank=True , null=True, verbose_name=_("Kategoriya tanlang"))
    image = models.ImageField(upload_to='homepage/images', blank=True, null=True, verbose_name=_("Rasim"))
    image_url = models.URLField(blank=True, null=True, verbose_name=_("URL Linki"))
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Status")) 
    site_sts =models.BooleanField(default=False, blank=True, verbose_name=_("Site STS"))
    site_rts =models.BooleanField(default=False, blank=True, verbose_name=_("Site RTS"))
      # filter product news
    cloudflare_id = models.CharField(max_length=200, blank=True, null=True)
    news = models.BooleanField(default=False, blank=True, verbose_name=_("Yangi Tavarlar ro'yxati"))
    # banner product add filter 
    banner_add = models.BooleanField(default=False, blank=True, verbose_name=_("Banner Tavarlar ro'yxati"))
    #  aksiya product 
    aksiya = models.BooleanField(default=False, blank=True, verbose_name=_("Aksiya Tavarlar ro'yxati"))
    xitlar = models.BooleanField(default=False, blank=True, verbose_name=_("Xitlar ro'yxati"))

    class Meta:
        verbose_name_plural = "Home Page Category"
        ordering = ["pk", "title", "top",]

    def __str__(self):
        return self.title
    
    @property
    def images_obj(self):
        if self.cloudflare_id:
            return get_image_url_from_cloudflare(self.cloudflare_id)
        else:
            if self.image:
                return site_name + self.image.url
            return None


    @classmethod
    def make_slug(cls, title):
        slug = slugify(title, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                title + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug
    
    def category(self):
        if self.mainCategory is not None:
            return f"{self.mainCategory.main_name}"
        return None
    
    @property
    def image_tag(self):
        if self.image is not None:
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image.url))
        else:
            return None


    def save(self, *args, **kwargs):
        self.title = self.title.title() if self.title else self.title
        self.slug = self.make_slug(self.title)
        if not self.cloudflare_id and self.image is not None:
            cload_id = upload_image_to_cloudflare(self.image.file)
            self.cloudflare_id = cload_id
        super().save(*args, **kwargs)