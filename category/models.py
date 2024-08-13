from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify
import random, string
from django.utils.translation import gettext_lazy as _

from category.utils import create_shortcode_super, create_shortcode_main, create_shortcode_sub  

from django.utils.html import format_html



class SuperCategory(models.Model):
    super_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    category_image = models.ImageField(
        upload_to="categories/super/imgs/",
        verbose_name=("Category Image"),
        blank=True,
        null=True,
        help_text=("Please use our recommended dimensions: 120px X 120px"),
    )
    slug = models.SlugField(unique=True, null=True, allow_unicode=True, editable=False, blank=True)
    super_image_content = models.ImageField(
        upload_to="category",
        blank=True,
        null=True,
        help_text=_("width: 1850px; height: 382px;"),
    )
    icon = models.FileField(
        upload_to="category",
        blank=True,
        null=True,
        help_text=_("max_widht:50, max_height:50"),
    )
    meta_name = models.CharField(max_length=200, blank=True, null=True)
    meta_content = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    seo_content = RichTextField(blank=True, null=True)
    sts_site = models.BooleanField(default=False)
    rts_site = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SuperCategory"
        ordering = ["pk", "super_name"]

    def __str__(self):
        return self.super_name

    @classmethod
    def make_slug(cls, super_name):
        slug = slugify(super_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                super_name + "-" + "".join(random.choices(letters, k=6)),
                allow_unicode=False,
            )
        return slug
    
    def image_tag(self):
        if self.category_image is not None:
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.category_image.url))
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None or self.slug == "":
            self.slug = slugify(self.super_name, allow_unicode=True)
            qs_exists = SuperCategory.objects.filter(
                slug=self.slug).exists()
            if qs_exists:
                self.slug = create_shortcode_super(self)

        super(SuperCategory, self).save(*args, **kwargs)

class MainCategory(models.Model):
    superCategory = models.ForeignKey(
        SuperCategory, on_delete=models.SET_NULL, null=True
    )
    main_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    main_image = models.ImageField(
        upload_to="categories/main/imgs/",
        verbose_name=(" Main Category Image"),
        blank=True,
        null=True,
    )
    slug = models.SlugField(unique=True,allow_unicode=True, null=True, editable=False, blank=True)
    icon = models.FileField(upload_to='category', blank=True, null=True)
    header_add = models.BooleanField(default=False, blank=True)
    main_meta = models.CharField(max_length=200, blank=True, null=True)
    ommabob = models.BooleanField(default=False, blank=True)
    main_content = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    sts_site = models.BooleanField(default=False)
    rts_site = models.BooleanField(default=False)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "MainCategory"
        ordering = ["pk", "main_name"]

    def __str__(self):
        return self.main_name

    @classmethod
    def make_slug(cls, main_name):
        slug = slugify(main_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                main_name + "-" + "".join(random.choices(letters, k=6)),
                allow_unicode=False,
            )
        return slug
    
    def image_tag(self):
        if self.main_image is not None:
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.main_image.url))
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None or self.slug == "":
            self.slug = slugify(self.main_name, allow_unicode=True)
            qs_exists = MainCategory.objects.filter(
                slug=self.slug).exists()
            if qs_exists:
                self.slug = create_shortcode_main(self)

        super(MainCategory, self).save(*args, **kwargs)


class SubCategory(models.Model):
    mainCategory = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    sub_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    sub_image = models.ImageField(
        upload_to="categories/main/imgs/",
        verbose_name=("Sub Category Image"),
        blank=True,
        null=True,
    )
    slug = models.SlugField(unique=True, null=True, allow_unicode=True,editable=False, blank=True)
    sub_meta = models.CharField(max_length=200, blank=True, null=True)
    sub_content = models.CharField(max_length=300, blank=True, null=True)
    seo_cub = RichTextField(blank=True, null=True)
    product_description = models.JSONField(blank=True, null=True)
    product_content = models.JSONField(blank=True, null=True)
    product_filter = models.JSONField(blank=True, null=True)
    sts_site = models.BooleanField(default=False)
    rts_site = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SubCategory"
        ordering = ["pk", "sub_name"]

    def __str__(self):
        return self.sub_name

    @classmethod
    def make_slug(cls, sub_name):
        slug = slugify(sub_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                sub_name + "-" + "".join(random.choices(letters, k=6)),
                allow_unicode=False,
            )
        return slug
    

    def image_tag(self):
        if self.sub_image is not None:
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.sub_image.url))
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None or self.slug == "":
            self.slug = slugify(self.sub_name, allow_unicode=True)
            qs_exists = SubCategory.objects.filter(
                slug=self.slug).exists()
            if qs_exists:
                self.slug = create_shortcode_sub(self)

        super(SubCategory, self).save(*args, **kwargs)
