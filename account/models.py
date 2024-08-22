from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.admin import display
from django.utils import timezone
from django.db import models
from datetime import date
from .manager import CustomUserManager 

from django.contrib.auth.models import Group


import requests 


# Create your models here.
class GouseUser(models.Model):
    token_uuid = models.CharField(max_length=200, blank=True, verbose_name=_("user uuid"))
    islogginIn = models.BooleanField(default=False, blank=True)
    divase = models.JSONField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    ip = models.CharField(max_length=12 ,blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    hostName = models.CharField(max_length=100, blank=True, default='web')
    create_at = models.DateField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    update_datetime = models.DateTimeField(auto_now=True, blank=True)
    userId = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.create_at is not None:
            self.create_at = date.today()
        return super().save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number.")
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True, verbose_name=_("phone")
    )
    first_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("first name")
    )
    last_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("last name")
    )
    is_login = models.BooleanField(default=False, blank=True) 
    login_date = models.DateField(null=True, blank=True)
    author = models.BooleanField(default=False, blank=True, verbose_name=_("author"))
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name=_("Special User")
    )
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_("date joined")
    )
    two_step_password = models.BooleanField(
        default=False, verbose_name=_("two step password"),
        help_text=_("is active two step password?"),
    )
    # userActive = models.BooleanField(default=False, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    @property
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    @display(
        boolean=True,
        description=_("Special User"),
    )
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PhoneOtp(models.Model):
    phone_regex = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number."),
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True, verbose_name=_("phone"),
    )
    otp = models.CharField(max_length=6)

    count = models.PositiveSmallIntegerField(default=0, help_text=_("Number of otp sent"))
    verify = models.BooleanField(default=False, verbose_name=_("is verify"))


    def __str__(self):
        return self.phone





class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name=_("Foydalanuvchi ID"))
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Shahri"))
    district = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Tuman"))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Manzil"))
    qavat = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Qavat"))
    lat = models.FloatField(blank=True, null=True, verbose_name=_("Latitud"))
    lon = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
    def __str__(self):
        return self.user.phone + " - " + self.city + " - " + self.district + " - " + self.address





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    passport_image = models.ImageField(upload_to="password/images/", blank=True, null=True)
    passportLocation_image = models.ImageField(upload_to="password/images/", blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    savdo_sum = models.BigIntegerField(blank=True, default=0)
    cashback_register = models.BooleanField(default=False, blank=True)
    foiz = models.PositiveIntegerField(blank=True, null=True)


    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



    def __str__(self):
        return self.user.phone
   


    @property
    def hamyon(self):
      url = f"https://hikvision-shop.uz/crm/user/hamyon/{self.user.phone}"
      res = requests.get(url=url)
      if not(res.json()["errors"]):
          return res.json()["data"]
      return None



    @property 
    def savdolar(self):
        url = f"https://hikvision-shop.uz/crm/user/savdolar/{self.user.phone}"
        res = requests.get(url=url)
        if not(res.json()["errors"]):
            return res.json()["data"]
        return None
    
    def get_total_savdo(self):
        pass 


    @property
    def total_savdo(self):
        pass 

    def get_foiz(self):
        pass 


