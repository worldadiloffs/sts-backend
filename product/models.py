from django.db import models
from category.models import SubCategory, SuperCategory, MainCategory
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import random, string
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import os
import requests
from django.conf import settings
import logging

# from product.servisses import get_image_url_from_cloudflare, upload_image_to_cloudflare
logger = logging.getLogger(__name__)

from .utils import  create_shortcode 

# ===========================
# 1) Cloudflare bilan ishlash funksiyalari
# ===========================

def upload_image_to_cloudflare(image_file):
    """
    image_file: Django ImageField orqali beriladigan fayl obyekti (masalan, instance.image).
    Cloudflare Images API'iga faylni yuboradi va qaytaradi:
    - Muvaffaqiyatli bo'lsa: Cloudflare tomonidan qaytarilgan image ID (string).
    - Aks holda: HTTPError yoki umumiy Exception (raise) bo'ladi.
    """
    # Cloudflare API endpoint: 
    account_id = settings.CLOUDFLARE_ACCOUNT_ID
    api_token = settings.CLOUDFLARE_API_KEY
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1"

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    # image_file.open("rb") — bu image_file bir FileField/ ImageField tomonidan saqlangan fayl patchi
    with image_file.open("rb") as file:
        files = {"file": (os.path.basename(image_file.name), file)}
        # Qo'shimcha ma'lumotlar qo'shmoqchi bo'lsangiz data={} dict orqali kiritsangiz ham bo'ladi.
        response = requests.post(endpoint, headers=headers, files=files, timeout=30)

    # Agar 4xx / 5xx kodli javob bo'lsa, raise HTTPError qiladi
    response.raise_for_status()

    json_data = response.json()
    if not json_data.get("success"):
        # Cloudflare return JSON formatiga qarab, errors[] ichida batafsil sabab bo'lishi mumkin
        errors = json_data.get("errors", [])
        raise Exception(f"Cloudflare Images API error: {errors}")

    # Natijadan image ID ni olib qaytaramiz
    return json_data["result"]["id"]


ALLOWED_VARIANTS = ["website", "mobile"]


def get_image_url_from_cloudflare(image_id, variant="website"):
    """
    Cloudflare Images domeni va account hash asosida rasm URL'ini hosil qiladi.
    variant: "website" yoki "mobile". 
    Agar variant noto'g'ri bo'lsa, default "website" olinadi.
    Misol: https://imagedelivery.net/{account_hash}/{image_id}/{variant}
    """
    domain = settings.CLOUDFLARE_IMAGES_DOMAIN  # masalan "imagedelivery.net"
    account_hash = settings.CLOUDFLARE_ACCOUNT_HASH

    if variant not in ALLOWED_VARIANTS:
        variant = "website"

    # https://imagedelivery.net/abcd1234xyz/abcdef1234567890/website
    return f"https://{domain}/{account_hash}/{image_id}/{variant}"

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    cloudflare_id = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(
        "product.Product", models.SET_NULL, null=True, related_name="images"
    )
    image = models.ImageField(upload_to="products", blank=False, null=True)
    # def save(self, *args, **kwargs):
    #     # Modelni oldindan saqlab qo'yamiz
    #     super().save(*args, **kwargs)
    #     # cload_bool =bool(bool(self.cloudflare_id is None) or not(self.cloudflare_id))
    #     # if cload_bool and self.image is not None:
    #     #     cload_id = upload_image_to_cloudflare(self.image.file)
    #     #     self.cloudflare_id = cload_id
    #     if bool(self.cloudflare_id is None or self.cloudflare_id == '') and self.image is not None:
    #         cload_id = upload_image_to_cloudflare(self.image.file)
    #         self.cloudflare_id = cload_id
    #     super().save(*args, **kwargs)
    

    #  # productni oldindan saqlab qo'yamiz


    # @property
    # def get_mobile(self):
    #     if not self.cloudflare_id:
    #         return None
    #     cloudflare_id = self.cloudflare_id
    #     img_url = get_image_url_from_cloudflare(cloudflare_id, variant="mobile")
    #     return img_url
    

    # @property
    # def get_admin_image(self):
    #     if not self.cloudflare_id:
    #         return ""
    #     cloudflare_id = self.cloudflare_id
    #     img_url = get_image_url_from_cloudflare(cloudflare_id, variant="mobile")
    #     return img_url

    

    # def display_image_admin(self):
    #     if not self.cloudflare_id:
    #         return ""
    #     cloudflare_id = self.cloudflare_id
    #     img_url = get_image_url_from_cloudflare(cloudflare_id, variant="mobile")
    #     img_html = f'<img src="{img_url}">'
    #     return format_html(img_html)
    def save(self, *args, **kwargs):
        """
        1) Avvalo, modelni birinchi bor saqlab, mahalliyga yozamiz (ImageField orqali fayl MEDIA_ROOT/products/...).
        2) Keyin, agar cloudflare_id bo'sh bo'lsa va image bor bo'lsa, Cloudflare Images API'iga yuklashga urinib ko'ramiz.
           Agar muvaffaqiyat bo'lsa, cloudflare_id ni yangilab yana saqlaymiz.
           Agar yuklashda xatolik bolsa, uni logga yozamiz (lekin exception tashlamaymiz),
           shunda rasm mahalliyga saqlangani qoladi, cloudflare_id bo'sh bo'ladi.
        """
        # 1) Birinchi save: faqat mahalliy média papkasiga saqlash
        is_new = not bool(self.pk)  # agar self.pk bo'lmasa, yangi ro'yxat
        super().save(*args, **kwargs)

        # 2) Agar rasm fayliga ega bo'lsak va cloudflare_id avvaldan mavjud bo'lmasa:
        if self.image and (not self.cloudflare_id or self.cloudflare_id.strip() == ""):
            try:
                # Cloudflare API'iga yuklash (burada image_file = self.image)
                new_id = upload_image_to_cloudflare(self.image)
                self.cloudflare_id = new_id

                # Faqat cloudflare_id ni yangilash uchun keyin save
                # update_fields=["cloudflare_id"] — shunchaki bitta maydonni yozish
                super().save(update_fields=["cloudflare_id"])

                logger.info(f"[Cloudflare] Rasm muvaffaqiyatli yuklandi: ID = {new_id}, Image# {self.pk}")
            except Exception as e:
                # Cloudflare'dan olingan xatoni logga yozamiz,
                # lekin exception tashlamaymiz (shuning uchun mahalliy saqlash davom etadi).
                logger.error(f"[Cloudflare] Rasm yuklash xatosi: {e}", exc_info=True)
                # cloudflare_id bo'sh qoladi va rasm mahalliy saqlanganicha qoladi.

    @property
    def get_mobile(self):
        """
        Agar Cloudflare'da ID bo'lsa, mobile variant URL'ini qaytaradi, aks holda None.
        Admin paneli yoki front-end uchun kerak bo'lishi mumkin.
        """
        if not self.cloudflare_id:
            return None
        return get_image_url_from_cloudflare(self.cloudflare_id, variant="mobile")

    @property
    def get_admin_image(self):
        """
        Admin panelida ('django.contrib.admin') list_display yoki boshqa joylarda
        rasmni kichik o'lchamda ko'rsatish uchun URL qaytaradi.
        """
        if not self.cloudflare_id:
            return ""
        return get_image_url_from_cloudflare(self.cloudflare_id, variant="mobile")

    def display_image_admin(self):
        """
        Admin panelida HTML orqali img tegini chiqarish uchun:
        {% for image in product.images.all %} {{ image.display_image_admin|safe }} {% endfor %}
        """
        if not self.cloudflare_id:
            return ""
        img_url = get_image_url_from_cloudflare(self.cloudflare_id, variant="mobile")
        # width/height / style parametrlari adminga mos qilib o'zgartiring
        return format_html(f'<img src="{img_url}" width="100" height="75" style="border-radius:2px;" />')

    def __str__(self):
        return self.title or f"Image #{self.pk}"
    


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
    
    site_sts = models.BooleanField(default=False, blank=True, db_index=True)
    
    site_rts = models.BooleanField(default=False, blank=True, db_index=True)
    
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

    cash_foiz = models.PositiveIntegerField(blank=True, null=True, editable=False)


    def cart_title(self, obj):
        if self.news:
            return self.news_title
        

    # @property
    # def cloud_id(self):
    #     obj = self.images.first()
    #     if obj and obj.image:
    #         if obj.cloudflare_id:
    #             return obj.cloudflare_id
    #     return None
    @property
    def cloud_id(self):
        """
        Product ga tegishli birinchi Image obyektining cloudflare_id ni qaytaradi, agar mavjud bo'lsa.
        """
        first_image = self.images.first()
        if first_image and first_image.cloudflare_id:
            return first_image.cloudflare_id
        return None
    
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
    
    
    # @property
    # def image(self):
    #     obj = self.images.first()
    #     if obj and obj.image:
    #         if obj.cloudflare_id:
    #             return get_image_url_from_cloudflare(obj.cloudflare_id, variant='mobile')
    #         return obj.image.url
    #     return None
    @property
    def image(self):
        """
        Front-end yoki boshqa contextlarda fasllarning rasmini olish uchun:
        1) Agar cloudflare_id mavjud bo'lsa, u holda Cloudflare URL'ini qaytaradi.
        2) Aks holda, mahalliy MEDIA_URL orqali saqlangan fayl URL'ini qaytaradi.
        """
        first_image = self.images.first()
        if first_image and first_image.image:
            if first_image.cloudflare_id:
                # Cloudflare variant: "website" deb qo'yamiz yoki kerakli variantni uzatish mumkin
                return get_image_url_from_cloudflare(first_image.cloudflare_id, variant="website")
            # Agar cloudflare_id bo'lmasa, Django MEDIA_URL orqali local faylni qaytaramiz:
            return first_image.image.url
        return None

    def image_tag(self):
        """
        Admin panelida 'list_display' da tasvirni ko'rsatish uchun:
        image_tag = '<img src="..." width="100" height="75" />'
        """
        url = self.image
        if not url:
            return ""
        return format_html(f'<img src="{url}" width="100" height="75" style="border-radius:2px;" />')
    
    def get_images(self):
        obj =  self.images.first()
        if obj:
            url = obj.get_admin_image
            return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(url))
        return ""

    # def image_tag(self):
    #     return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image))
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


