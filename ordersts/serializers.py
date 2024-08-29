from rest_framework import serializers

from .models import Order, OrderItem
from config.settings import site_name


class OrderItemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_images(self, obj):
        images = obj.product.images.all()
        if images:
            return [site_name +  image.image.url  for image in images]
        

    def get_price(self, obj):
        if obj.product.price:
            return obj.product.price





class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"




  

    



#  STATUS_CHOICES = (
#         ('pending', "Yig'ilyapti"),
#         ('processing', 'Yetkazilyapti'),
#         ('shipped', "Yetkazildi"),
#         ('delivered', "Xaridorga berildi"),
#     )
#     yetkazish = models.DateField(blank=True, null=True, verbose_name=_("Yetkazish sanasi"))
#     tolov_usullar = models.ForeignKey(TolovUsullar, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("To'lov usullari"))
#     punkit = models.ForeignKey(Dokon, on_delete=models.CASCADE, related_name='Manzil', blank=True, null=True, verbose_name=_(" Yetkazib beriladigan dokon Manzil"))
#     zakas_id = models.IntegerField(blank=True, unique=True, verbose_name=_("Buyurtma raqami") )
#     cashback = models.FloatField(blank=True, null=True, verbose_name=_("Cashback  yechgan summa"))
#     depozit = models.FloatField(blank=True, null=True, verbose_name=_("Depozit yechgan summasi"))
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Qanday to'lov qilish"))
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_("Buyurtma statusi"))
#     user = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, verbose_name=_("Buyurtma Bergan Foydalanuvchi"))
#     shahar = models.ForeignKey(Shaharlar, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Shahar"))
#     tuman = models.ForeignKey(Tumanlar, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Tuman"))
#     qishloq = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Qishloq"))
#     uy_nomer = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Uy nomer"))
#     order_items = models.ManyToManyField(OrderItem,  blank=True, verbose_name=_("Savdo qilingan mahsulotlar"))
#     dastafka_summa = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Dastafka summasi"))
#     # teskor_buyurtma_time = models.DateTimeField(blank=True, null=True, verbose_name=_("Teskor buyurtma vaqt"))
#     teskor_buyurtma = models.BooleanField(default=False, blank=True)
#     total_price = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_("Buyurtma narxi"))
#     comment = models.CharField(max_length=200,blank=True, null=True, verbose_name=_("Buyurtma uchun admin  xabarlari"))
#     firma_buyurtma = models.ForeignKey(FirmaBuyurtma, on_delete=models.SET_NULL , blank=True, null=True, verbose_name=_("Firma buyurtma"))
#     # firma_name = models.CharField(max_length=255, blank=True, verbose_name=_("Firma nomi"))
#     vazvrat_product = models.ManyToManyField(VazvratProdcut, blank=True, verbose_name=_("Qaytarilgan Mahsulotlar") )
#     site_sts = models.BooleanField(default=False, blank=True, verbose_name=_("STS SITE"))
#     site_rts = models.BooleanField(default=False, blank=True, verbose_name=_("RTS SITE"))
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Savdo qilingan vaqt"))
#     updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name=_("Ozgartirilgan vaqt"))
#     is_finished = models.BooleanField(default=False, blank=True, verbose_name=_("Buyurtma tolov statusi"))
#     cencel = models.BooleanField(default=False, blank=True, verbose_name=_("Buyurtma bekor qilinganmi"))
#     xodim = models.ForeignKey(Xodim, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Xodim"), editable=False)




class OrderGetSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = "__all__"



data = {
    "Buyurtma_raqami": "123456",
    "status": "bekor",
    "Buyurtma_vaqti": "2022-01-01 10:00:0",
    "Yetkazib_berish_vaqti": "2022-01",
    "Tolov_usuli": "Karta",
    "Qabul_qilish_usuli": "yetkazib berish",
    "Buyurtma_turi": "onliyn",
    "Yetkazib_berish_manzili": "Jizzi",
    "narxi": "43443434343 summa",
    "yetkazib_berish": 0,
    "Jami": 0,
}


class OrderGetUserSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    order_obj = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

    def get_order_obj(self, obj):
        yetkazib_berish_manzili = obj.punkit and obj.punkit.name or (obj.qishloq and obj.qishloq or "")
        tolov_usuli = obj.tolov_usullar and obj.tolov_usullar.name or ""
        narxi = obj.total_price and obj.total_price or 0 
        yetkazib_berish = obj.dastafka_summa and obj.dastafka_summa or 0 
        status = obj.status and obj.status or ""
        status_color = "blue" if status == "pending" else "green"
        yetkazish_vaqti = obj.yetkazish and obj.yetkazish.strftime("%Y-%m-%d %H:%M:%S") or "90 minutov"
        data = {
            "Buyurtma raqami": obj.zakas_id,
            "status": status,
            "Buyurtma vaqti": obj.created_at,
            "Yetkazib berish vaqti": yetkazish_vaqti,
            "Tolov usuli": tolov_usuli,
            "Buyurtma turi": "onliyn",
            "Yetkazib berish manzili": yetkazib_berish_manzili,
            "Summa": narxi,
            "Yetkazib berish": yetkazib_berish,
            "Jami": narxi - yetkazib_berish,
            "status_color": status_color,
        }
        return data


        

        
    