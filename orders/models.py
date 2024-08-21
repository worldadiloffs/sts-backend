from django.db import models
from product.models import Product
from account.models import User, UserAddress
from settings.models import Dokon, Shaharlar , Tumanlar
from django.contrib.postgres.fields import ArrayField
from settings.models import PaymentMethod , TolovUsullar
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth import get_user_model



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', blank=True)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    serena = ArrayField(models.CharField(max_length=20, blank=True), blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_items', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    site_sts = models.BooleanField(default=True, blank=True)
    site_rts = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Savdo qilingan mahsulotlar"
        ordering = ["pk", "created_at"]

    def get_serena(self):
        return f''' {self.serena} ''' if self.serena else ''

    def __str__(self):
        return f'''{self.product.product_name}  : {self.quantity}   : {self.product.price} \n '''
    
    def save(self, *args, **kwargs):
        # if self.serena is not None:
        #     self.quantity = len(self.serena)
        # self.price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.quantity * self.product.price
    
    def get_product_name(self):
        return self.product.product_name if self.product else None
    
    def get_quantity(self):
        return self.quantity
    
class VazvratProdcut(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    serena = ArrayField(models.CharField(max_length=20, blank=True),blank=True, null=True)
    counts= models.PositiveIntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Vazvrat qilingan mahsulotlar"
        ordering = ["pk", "created_at"]



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', "Yig'ilyapti"),
        ('processing', 'Yetkazilyapti'),
        ('shipped', "Yetkazildi"),
        ('delivered', "Xaridorga berildi"),
    )
    yetkazish = models.DateField(blank=True, null=True)
    tolov_usullar = models.ForeignKey(TolovUsullar, on_delete=models.SET_NULL, blank=True, null=True)
    punkit = models.ForeignKey(Dokon, on_delete=models.CASCADE, related_name='Manzil', blank=True, null=True)
    zakas_id = models.IntegerField(blank=True, unique=True)
    cashback = models.FloatField(blank=True, null=True)
    depozit = models.FloatField(blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True)
    # addres = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, blank=True, null=True)
    shahar = models.ForeignKey(Shaharlar, on_delete=models.CASCADE, blank=True, null=True)
    tuman = models.ForeignKey(Tumanlar, on_delete=models.CASCADE, blank=True, null=True)
    qishloq = models.CharField(max_length=200, blank=True, null=True)
    uy_nomer = models.CharField(max_length=20, blank=True, null=True)
    order_items = models.ManyToManyField(OrderItem,  blank=True,)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    comment = models.CharField(blank=True, null=True)
    vazvrat_product = models.ManyToManyField(VazvratProdcut, blank=True, )
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_finished = models.BooleanField(default=False, blank=True)
    cencel = models.BooleanField(default=False, blank=True)
    # modified_by = models.CharField(max_length=200, blank=True, null=True)


    

    class Meta:
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at", "zakas_id"]

    def __str__(self):
        return f"Order {self.zakas_id} +  {self.user.phone}"
    

    def get_addres_address(self):
        return f"{self.addres.city} - {self.addres.district} - {self.addres.address}" if self.addres else None
    

    
    def save(self, *args, **kwargs):
        # self.total_price = sum(item.price for item in self.order_items.all())

        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.total_price
    
    def get_product_names(self):
        data = [item.get_product_name() for item in self.order_items.all()]
        return ''',  '''.join(data) if data else None

    
    
    def get_order_items(self):
        return self.order_items.all()
    
    def get_user_phone(self):
        return self.user.phone if self.user else None
    
    def get_status(self):
        return self.status.capitalize() if self.status else None
    
    def get_status_display(self):
        return self.STATUS_CHOICES[self.status.index('pending')][1] if self.status == 'pending' else self.status.capitalize()
    
    def get_created_at_display(self):
        return self.created_at.strftime('%d-%m-%Y %H:%M:%S')
    
    def get_updated_at_display(self):
        return self.updated_at.strftime('%d-%m-%Y %H:%M:%S')
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def get_total_items(self):
        return sum(item.quantity for item in self.order_items.all())