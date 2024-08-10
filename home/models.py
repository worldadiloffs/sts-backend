from django.db import models
from django.utils.translation import gettext_lazy as _
from category.models import MainCategory , SubCategory
from django.utils.text import slugify
import random, string
# Create your models here.
from config.settings import site_name


class Banner(models.Model):
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    status = models.BooleanField(default=False, blank=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='banner/images', blank=True)
    category = models.ForeignKey(MainCategory , on_delete=models.SET_NULL , blank=True, null=True)
    site_sts =models.BooleanField(default=False, blank=True)
    site_rts =models.BooleanField(default=False, blank=True)
    
    class Meta:
        verbose_name_plural = "Banner"
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
    


    def save(self, *args, **kwargs):
        self.title = self.title.title() if self.title else self.title
        self.slug = self.make_slug(self.title)
        super().save(*args, **kwargs)    


class HomePageCategory(models.Model):
    top= models.IntegerField(blank=True, null=True, help_text=_("home page nechinchi orinda chiqsin"))
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    title = models.CharField(max_length=200, blank=True)
    mainCategory = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, blank=True , null=True)
    # subcategory_filter = models.ManyToManyField(SubCategory , blank=True)
    image = models.ImageField(upload_to='homepage/images', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=False, blank=True) 
    site_sts =models.BooleanField(default=False, blank=True)
    site_rts =models.BooleanField(default=False, blank=True)
      # filter product news
    news = models.BooleanField(default=False, blank=True)
    # banner product add filter 
    banner_add = models.BooleanField(default=False, blank=True)
    #  aksiya product 
    aksiya = models.BooleanField(default=False, blank=True)
    xitlar = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name_plural = "homepageCategory"
        ordering = ["pk", "title", "top",]

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


    def save(self, *args, **kwargs):
        self.title = self.title.title() if self.title else self.title
        self.slug = self.make_slug(self.title)

        super().save(*args, **kwargs)


class homePage(models.Model):
    servis = models.BooleanField(default=False, blank=True)
    ustanofka = models.BooleanField(default=False, blank=True)
    maqola = models.BooleanField(default=False, blank=True)
    yetkazib_berish = models.BooleanField(default=False, blank=True)
    ads = models.BooleanField(default=False, blank=True)
    mobile_app = models.BooleanField(default=False, blank=True)
    site_sts =models.BooleanField(default=False, blank=True)
    site_rts =models.BooleanField(default=False, blank=True)
