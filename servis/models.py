from django.db import models
from config.settings import site_name
from ckeditor.fields import RichTextField
# - card
class JopServisCard(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    image = models.ImageField(upload_to='jop_servis_images/')
    jopservis = models.ForeignKey('servis.JopServis', models.SET_NULL, blank=True, null=True, related_name='jopserviscards')

    @property
    def get_image(self):
        if self.image:
            return site_name + self.image.url
        return None

class JopServis(models.Model):
    header_title = models.CharField(max_length=200)
    header_title_text = models.TextField(max_length=200)
    bground_image = models.ImageField(upload_to='jop_servis_images/', blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)

    @property
    def get_bground_image(self):
        if self.bground_image:
            return site_name + self.bground_image.url
        return None
    
    def __str__(self):
        return self.header_title

class AboutServisCard(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    image = models.FileField(upload_to='about_servis_images/', blank=True, null=True)
    jopservis = models.ForeignKey('servis.AboutServis', models.SET_NULL, blank=True, null=True, related_name='aboutserviscards')
    
    @property
    def get_image(self):
        if self.image:
            return site_name + self.image.url
        return None
    
    


class AboutServis(models.Model):
    title = models.CharField(max_length=200)
    bground_image = models.ImageField(upload_to='about_servis_images/')
    status = models.BooleanField(default=False, blank=True)

    @property
    def get_bground_image(self):
        if self.bground_image:
            return site_name + self.bground_image.url
        return None



class PriceServisCard(models.Model):
    content = models.TextField(max_length=500, blank=True , null=True)
    narx = models.PositiveIntegerField(blank=True, null=True)
    arzonlashgan_narx = models.PositiveIntegerField(blank=True, null=True)
    product_content = models.TextField(blank=True, null=True)
    priceservis = models.ForeignKey('servis.PriceServis', models.SET_NULL, blank=True, null=True, related_name='priceserviscards')



class PriceServis(models.Model):
    title = models.CharField(max_length=200)
    # price = models.PositiveIntegerField(blank=True)
    # discount_price = models.PositiveIntegerField(blank=True,null=True)
    bground_image = models.ImageField(upload_to='price_servis_images/', blank=True, null=True, )

    @property
    def get_bground_image(self):
        if self.bground_image:
            return site_name + self.bground_image.url
        return None


class UstanofkaServisCard(models.Model):
    title = models.CharField(max_length=200)
    time_jop = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    problem = models.TextField(max_length=500, blank=True, null=True)
    solution = models.TextField(max_length=500, blank=True, null=True)
    jopservis = models.ForeignKey('servis.UstanofkaServis', models.SET_NULL, blank=True, null=True, related_name='ustanofkaserviscards')

class UstanofkaServis(models.Model):
    '''Реализованные проекты: Наши кейсы по установке видеонаблюдения '''
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    bground_image = models.ImageField(upload_to='ustanofka_servis_images/', blank=True, null=True)

    @property
    def get_bground_image(self):
        if self.bground_image:
            return site_name + self.bground_image.url
        return None
        


class KomandaServisCard(models.Model):
    ism = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='komanda_servis_images/', blank=True, null=True)
    yil = models.PositiveIntegerField(blank=True, default=3)
    komandaservis = models.ForeignKey('servis.KomandaServis', models.SET_NULL, blank=True, null=True, related_name='komandaserviscard')

    @property
    def get_image(self):
        if self.image:
            return site_name + self.image.url
        return None
        

class KomandaServis(models.Model):
    '''Наша команда '''
    title = models.CharField(max_length=200, default='comanda')
    description = models.TextField(max_length=500, blank=True, null=True)
    bground_image = models.ImageField(upload_to='komanda_servis_images/', blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)

    @property
    def get_bground_image(self):
        if self.bground_image:
            return site_name + self.bground_image.url
        return None



class LisenceServisCard(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lisence_servis_images/', blank=True)
    lisenceservis = models.ForeignKey('servis.LisenceServis', models.SET_NULL, blank=True, null=True, related_name='lisenceserviscards')

    @property
    def get_image(self):
        if self.image:
            return site_name + self.image.url
        return None
        


class LisenceServis(models.Model):
    '''Лицензии '''
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    bground_image = models.ImageField(upload_to='lisence_servis_images/', blank=True, null=True)

    @property
    def get_bground_image(self):
        if self.bground_image:
            return site_name + self.bground_image.url
        return None




class KontaktServis(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)


class CategoryServisCard(models.Model):
    title = models.CharField(max_length=200)
    link_url = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='category_servis_images/', blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    category = models.ForeignKey('servis.CategoryServis', models.SET_NULL, blank=True, null=True, related_name='children')


    @property
    def get_image(self):
        if self.image:
            return site_name + self.image.url
        return None
        


class CategoryServis(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category_servis_images/', blank=True, null=True)
    # link = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def get_image(self):
        if self.image:
            return site_name + self.image.url
        
        return None
    


class SavolJavobServis(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=500)
    status = models.BooleanField(default=False, blank=True)




class ContactContentServis(models.Model):
    phone = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=300)
    telegram = models.URLField(max_length=200, blank=True, null=True)
    working_hours = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    youtube = models.URLField(max_length=200, blank=True, null=True)
