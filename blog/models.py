from django.db import models
from ckeditor.fields import RichTextField
from category.models import MainCategory , SubCategory 
from django.utils.text import slugify
import random, string

# Create your models here.

class BlogCategory(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='blogcategory', blank=True)
    status = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
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

class Tag(models.Model):
    title = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True, null=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)




class BlogItem(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='blogitems', blank=True)
    content = RichTextField(blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.ManyToManyField(Tag , blank=True)
    status = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    create_at = models.DateField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

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



class BlogHome(models.Model):
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    image = models.ImageField(upload_to='blog', blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL , blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    create_at = models.DateField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

    
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


