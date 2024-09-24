from django.db import models
# - card
class JopServisCard(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    image = models.ImageField(upload_to='jop_servis_images/')
    jopservis = models.ForeignKey('servis.JopServis', models.SET_NULL, blank=True, null=True)

class JopServis(models.Model):
    header_title = models.CharField(max_length=200)
    header_title_text = models.TextField(max_length=200)
    bground_image = models.ImageField(upload_to='jop_servis_images/', blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)

class AboutServisCard(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    image = models.FileField(upload_to='about_servis_images/', blank=True, null=True)
    jopservis = models.ForeignKey('servis.JopServis', models.SET_NULL, blank=True, null=True)


class AboutServis(models.Model):
    title = models.CharField(max_length=200)
    bground_image = models.ImageField(upload_to='about_servis_images/')
    status = models.BooleanField(default=False, blank=True)


class PriceServisCard(models.Model):
    product_name = models.CharField(max_length=200)
    count = models.PositiveIntegerField(blank=True)
    priceservis = models.ForeignKey('servis.PriceServis', models.SET_NULL, blank=True, null=True)



class PriceServis(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField(blank=True)
    discount_price = models.PositiveIntegerField(blank=True,null=True)
    bground_image = models.ImageField(upload_to='price_servis_images/', blank=True, null=True)


class UstanofkaServisCard(models.Model):
    title = models.CharField(max_length=200)
    time_jop = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    problem = models.TextField(max_length=500, blank=True, null=True)
    solution = models.TextField(max_length=500, blank=True, null=True)
    jopservis = models.ForeignKey('servis.UstanofkaServis', models.SET_NULL, blank=True, null=True)

class UstanofkaServis(models.Model):
    '''Реализованные проекты: Наши кейсы по установке видеонаблюдения '''
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    bground_image = models.ImageField(upload_to='ustanofka_servis_images/', blank=True, null=True)


class KomandaServisCard(models.Model):
    ism = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='komanda_servis_images/', blank=True, null=True)
    yil = models.PositiveIntegerField(blank=True, default=3)
    komandaservis = models.ForeignKey('servis.KomandaServis', models.SET_NULL, blank=True, null=True)

class KomandaServis(models.Model):
    '''Наша команда '''
    title = models.CharField(max_length=200, default='comanda')
    description = models.TextField(max_length=500, blank=True, null=True)
    bground_image = models.ImageField(upload_to='komanda_servis_images/', blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)



class LisenceServisCard(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lisence_servis_images/', blank=True)
    lisenceservis = models.ForeignKey('servis.LisenceServis', models.SET_NULL, blank=True, null=True)


class LisenceServis(models.Model):
    '''Лицензии '''
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    bground_image = models.ImageField(upload_to='lisence_servis_images/', blank=True, null=True)




class KontaktServis(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)


class CategoryServisCard(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category_servis_images/', blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    category = models.ForeignKey('servis.CategoryServis', models.SET_NULL, blank=True, null=True, related_name='children')


class CategoryServis(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category_servis_images/', blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)