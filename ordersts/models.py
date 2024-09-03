from django.db import models
from product.models import Product
from account.models import User, UserAddress
from settings.models import Dokon, OrderSetting, Shaharlar , Tumanlar
from django.contrib.postgres.fields import ArrayField
from settings.models import PaymentMethod , TolovUsullar
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from xodimlar.models import Xodim
from cashback.models import CashbackKard
from config.settings import site_name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name=_("Mahsulotlar"), blank=True)
    quantity = models.PositiveIntegerField(default=1, blank=True, verbose_name=_("Soni"))
    serena = ArrayField(models.CharField(max_length=20, blank=True), blank=True, null=True, verbose_name=_("Mahsulot serena nomerlari"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_items', verbose_name=_("Foydalanuvchi"), blank=True)
    zakas_id = models.IntegerField(blank=True, null=True)
    mahsul0t_narxi = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Mahsulot narxi"))
    site_sts = models.BooleanField(default=True, blank=True, verbose_name=_('STS SITE'))
    site_rts = models.BooleanField(default=True, blank=True, verbose_name=_('RTS SITE'))
    created_at = models.DateTimeField(auto_now_add=True , verbose_name=_('Savdo qilingan vaqt'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Ozgartirilgan vaqt'))

    
    class Meta:
        verbose_name_plural = "Savdo qilingan mahsulotlar"
        ordering = ["pk", "created_at"]

    def get_serena(self):
        return f''' {self.serena} ''' if self.serena else ''

    def __str__(self):
        return f'''{self.product.product_name}  : {self.quantity}   : {self.product.price} \n '''
    
    def save(self, *args, **kwargs):
        if self.mahsul0t_narxi is None:
            doller = OrderSetting.objects.first()
            doller_value =int(doller.doller * doller.nds / 10)
            self.mahsul0t_narxi = (self.product.price * doller_value) 
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.quantity * self.product.price
    
    def get_product_name(self):
        return self.product.product_name if self.product else None
    
    def get_quantity(self):
        return self.quantity
    
class VazvratProdcut(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True , verbose_name=_("Mahsulot ID"))
    mahsulot_narxi = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Mahsulot narxi"))
    serena = ArrayField(models.CharField(max_length=20, blank=True),blank=True, null=True, verbose_name=_("Mahsulot serena nomerlar"))
    zakas_id = models.IntegerField(blank=True, null=True, verbose_name=_("Buyurtma raqami"))
    counts = models.PositiveIntegerField(default=1, blank=True, null=True, verbose_name=_("Soni"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Savdo qilingan vaqt"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Ozgartirilgan vaqt"))
    site_sts = models.BooleanField(default=True, blank=True, verbose_name=_('STS SITE'))
    site_rts = models.BooleanField(default=True, blank=True, verbose_name=_('RTS SITE'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Foydalanuvchi"))





    def vazvrat_product(self):
        return {
            "product_name": self.product_id.product_name,
            "product_image": self.product_id.image and(site_name + self.product_id.image.url) or None,
            "mahsulot_narxi": self.mahsulot_narxi,
            "serena": self.serena,
            "counts": self.counts,
            "created_at": self.created_at.strftime("%Y-%m-%d"),
        }

    def __str__(self):
        return f'''{self.product_id.product_name}  : {self.counts}   : {self.product_id.price} \n '''
    class Meta:
        verbose_name_plural = "Vazvrat qilingan mahsulotlar"
        ordering = ["pk", "created_at"]


    def save(self, *args, **kwargs):
        if self.zakas_id is None:
            raise ValueError("Buyurtma raqami bo'sh bo'lmasligi kerak")
        super().save(*args, **kwargs)

class FirmaBuyurtma(models.Model):
    firma_name = models.CharField(max_length=255, blank=True, verbose_name=_("Firma nomi"))
    buyurtma_raqami = models.IntegerField(blank=True, unique=True, verbose_name=_("Buyurtma raqami") )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Foydalanuvchi"))
    inn_nomer = models.CharField(max_length=12, blank=True, null=True,verbose_name=_("INN nomer"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Savdo qilingan vaqt"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Ozgartirilgan vaqt"))
    shartnoma_file = models.FileField(upload_to='shartnoma/', blank=True,null=True, verbose_name=_("Sharhnoma file"))
    shartnoma_status = models.BooleanField(default=False, verbose_name=_("Sharhnoma statusi"))
    site_sts = models.BooleanField(default=False, blank=True, verbose_name=_('STS SITE'))
    site_rts = models.BooleanField(default=False, blank=True, verbose_name=_('RTS SITE'))



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', "Yig'ilyapti"),
        ('processing', 'Yetkazilyapti'),
        ('shipped', "Yetkazildi"),
        ('delivered', "Xaridorga berildi"),
        ('cencel', "Bekor Qilindi"),
    )
    yetkazish = models.DateField(blank=True, null=True, verbose_name=_("Yetkazish sanasi"))
    tolov_usullar = models.ForeignKey(TolovUsullar, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("To'lov usullari"))
    punkit = models.ForeignKey(Dokon, on_delete=models.CASCADE, related_name='Manzil', blank=True, null=True, verbose_name=_(" Yetkazib beriladigan dokon Manzil"))
    zakas_id = models.IntegerField(blank=True, unique=True, verbose_name=_("Buyurtma raqami") )
    cashback = models.FloatField(blank=True, null=True, verbose_name=_("Cashback  yechgan summa"))
    tushadigan_cash_summa = models.FloatField(blank=True, null=True, editable=False, verbose_name=_("Tushadigan cash summasi"))
    depozit = models.FloatField(blank=True, null=True, verbose_name=_("Depozit yechgan summasi"))
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Qanday to'lov qilish"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_("Buyurtma statusi"))
    user = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, verbose_name=_("Buyurtma Bergan Foydalanuvchi"))
    shahar = models.ForeignKey(Shaharlar, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Shahar"))
    tuman = models.ForeignKey(Tumanlar, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Tuman"))
    qishloq = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Qishloq"))
    uy_nomer = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Uy nomer"))
    order_items = models.ManyToManyField(OrderItem,  blank=True, verbose_name=_("Savdo qilingan mahsulotlar"))
    dastafka_summa = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Dastafka summasi"))
    teskor_buyurtma = models.BooleanField(default=False, blank=True)
    total_price = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_("Buyurtma narxi"))
    comment = models.CharField(max_length=200,blank=True, null=True, verbose_name=_("Buyurtma bekor qilingan natija"))
    firma_buyurtma = models.ForeignKey(FirmaBuyurtma, on_delete=models.SET_NULL , blank=True, null=True, verbose_name=_("Firma buyurtma"))
    vazvrat_product = models.ManyToManyField(VazvratProdcut, blank=True, verbose_name=_("Qaytarilgan Mahsulotlar") )
    site_sts = models.BooleanField(default=False, blank=True, verbose_name=_("STS SITE"))
    site_rts = models.BooleanField(default=False, blank=True, verbose_name=_("RTS SITE"))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Savdo qilingan vaqt"))
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name=_("Ozgartirilgan vaqt"))
    is_finished = models.BooleanField(default=False, blank=True, verbose_name=_("Buyurtma tolov statusi"))
    cencel = models.BooleanField(default=False, blank=True, verbose_name=_("Buyurtma bekor qilinganmi"))
    xodim = models.ForeignKey(Xodim, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Xodim"), editable=False)
    order_close = models.BooleanField(default=False, blank=True, verbose_name=_("Buyurtma Yopish"))


    

    class Meta:
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at", "zakas_id"]



    def __str__(self):
        return f"Order {self.zakas_id} +  {self.user.phone}"
        

    
    def save(self, *args, **kwargs):
        if self.is_finished and self.status == 'delivered':
            if not self.order_close:
                self.order_close = True
                if self.tushadigan_cash_summa is not None:
                    cash = CashbackKard.objects.filter(user=self.user, site_sts=self.site_sts, site_rts=self.site_rts).first()
                    if cash is not None:
                        if cash.hisobot is not None:
                            cash_summa = True
                            for his in cash.hisobot:
                                if int(self.zakas_id) == int(his['zakas_id']):
                                    cash_summa = False
                            if cash_summa:
                                cash.balance  += self.tushadigan_cash_summa
                                cash.hisobot.append({"zakas_id": self.zakas_id, "summa": self.tushadigan_cash_summa, "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') , "hisob": "+"})
                                cash.save()
                        
                        else:
                            cash.balance  += self.tushadigan_cash_summa
                            cash.hisobot = [{"zakas_id": self.zakas_id, "summa": self.tushadigan_cash_summa , "created_at": self.created_at.strftime('%Y-%m-%d %H:%M'), "hisob": "+"}]
                        cash.save()
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