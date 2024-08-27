from django.db import models
from ckeditor.fields import RichTextField
from category.models import MainCategory , SubCategory 
from django.utils.text import slugify
import random, string

from django.utils.translation import gettext_lazy as _


# Create your models here.

class BlogCategory(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name=_("Kategoriya nomi"))
    image = models.ImageField(upload_to='blogcategory', blank=True, verbose_name=_("Rasm"))
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Status"))
    site_sts = models.BooleanField(default=False, blank=True,)
    site_rts = models.BooleanField(default=False, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)


    class Meta:
        verbose_name_plural = "Blog Kategorileri"
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

class Tag(models.Model):
    title = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True, null=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name_plural = "Blog Taglar"
        ordering = ["pk", "title"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)




class BlogItem(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Blog nomi"))
    image = models.ImageField(upload_to='blogitems', blank=True, verbose_name=_("Rasm"))
    content = RichTextField(blank=True, verbose_name=_("Blog uchun malumot"))
    blogcategory = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Kategoriya"))
    tag = models.ManyToManyField(Tag , blank=True, verbose_name=_("Taglar"))
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Status"))
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    create_at = models.DateField(auto_now_add=True, blank=True, verbose_name=_("Yaratilgan vaqti"))
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name=_("Yangilanish vaqti"))

    class Meta:
        verbose_name_plural = "Bloglar"
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



class BlogHome(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name=_("Home sayti blog nomi"))
    text = models.TextField(blank=True, null=True, verbose_name=_("Home sayti blog uchun malumot"))
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Status"))
    image = models.ImageField(upload_to='blog', blank=True, verbose_name=_("Rasm"))
    site_sts = models.BooleanField(default=False, blank=True,)
    site_rts = models.BooleanField(default=False, blank=True)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL , blank=True, null=True, verbose_name=_("Kategoriya"))
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True,)
    create_at = models.DateField(auto_now_add=True, blank=True, verbose_name=_("Yaratilgan vaqti"))
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name=_("Yangilanish vaqti"))

    
    class Meta:
        verbose_name_plural = "Asosiy oyna uchun Bloglar"
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


