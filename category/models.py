from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
import random, string
from django.utils.translation import gettext_lazy as _

from category.utils import create_shortcode_super, create_shortcode_main, create_shortcode_sub  

from django.utils.html import format_html




class SuperCategory(models.Model):
    rating = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Rating"))
    super_name = models.CharField(max_length=200, blank=False, null=False, unique=True, verbose_name=_("Asosiy Kategoriya Nomi"))
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
        verbose_name=_("Icon"),
    )
    meta_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Meta uchun nom"))
    meta_content = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Meta uchun  content"))
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Site chiqish uchun status"))
    seo_content = RichTextField(blank=True, null=True, verbose_name=_("SEO uchun  Content"))
    sts_site = models.BooleanField(default=False, verbose_name=_("Site STS uchun status"))
    rts_site = models.BooleanField(default=False, verbose_name=_("Site RTS uchun status"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))

    class Meta:
        verbose_name_plural = "Asosiy Kategoriyalar"
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
        if self.category_image:
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

        if not self.sts_site and not self.rts_site:
            raise ValidationError("At least one site status should be checked")

        super(SuperCategory, self).save(*args, **kwargs)




class MainCategory(models.Model):
    rating = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Rating"))
    superCategory = models.ForeignKey(
        SuperCategory, on_delete=models.SET_NULL, null=True , verbose_name=_("Asosiy Kategoriya"))
    main_name = models.CharField(max_length=200, blank=False, null=False, unique=True, verbose_name=_("Kategoriya uchun nom"))
    main_image = models.ImageField(
        upload_to="categories/main/imgs/",
        verbose_name=("Kategoriya rasm"),
        blank=True,
        null=True,
    )
    slug = models.SlugField(unique=True,allow_unicode=True, null=True, editable=False, blank=True)
    icon = models.FileField(upload_to='category', blank=True, null=True, verbose_name=_("Icon"))
    header_add = models.BooleanField(default=False, blank=True, verbose_name=_("Headerga qo'shish uchun status"))
    main_meta = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Meta uchun nom"))
    ommabob = models.BooleanField(default=False, blank=True, verbose_name=_("Ommabob Tavarlar uchun status"))
    main_content = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Kategoriya uchun  content"))
    status = models.BooleanField(default=False, blank=True, verbose_name=_("Site chiqish uchun status"))
    sts_site = models.BooleanField(default=False, verbose_name=_("Site STS uchun status"))
    rts_site = models.BooleanField(default=False, verbose_name=_("Site RTS uchun status"))
    created = models.DateTimeField(blank=True, null=True, verbose_name=_("Yaratilgan vaqti"))

    class Meta:
        verbose_name_plural = "Main Kategoriyalar"
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
        if self.main_image:
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
        if not(self.sts_site or self.rts_site):
            raise ValidationError("At least one of 'STS_site' or 'RTS_site' must be True")
        super(MainCategory, self).save(*args, **kwargs)






class SubCategory(models.Model):
    rating = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Rating"))
    mainCategory = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Main Kategoriya")
    )
    sub_name = models.CharField(max_length=200, blank=False, null=False, unique=True, verbose_name=_("Sub Kategoriya uchun nom")) 
    sub_image = models.ImageField( upload_to="categories/main/imgs/", verbose_name=("Sub Kategoriya rasm"), blank=True, null=True) 
    slug = models.SlugField(unique=True, null=True, allow_unicode=True,editable=False, blank=True)
    sub_meta = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Meta uchun nom"))
    sub_content = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Sub Kategoriya uchun  content"))
    seo_cub = RichTextField(blank=True, null=True, verbose_name=_("SEO uchun  Content"))
    product_description = models.JSONField(blank=True, null=True, verbose_name=_("Tegishli tavarlar uchun qiymatlar"))
    product_content = models.JSONField(blank=True, null=True, verbose_name=_("Tegishli tavarlar uchun short  qiymatlar"))
    sts_site = models.BooleanField(default=False, verbose_name=_("Site STS uchun status"))
    rts_site = models.BooleanField(default=False, verbose_name=_("Site RTS uchun status"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))    

    class Meta:
        verbose_name_plural = "Sub Kategoriyalar"
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
        if self.sub_image:
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
        if not(self.sts_site) and not(self.rts_site):
            raise ValueError({"data": "errors"})

        super(SubCategory, self).save(*args, **kwargs)
