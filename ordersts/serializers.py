from rest_framework import serializers

from settings.models import OrderSetting 
from django.core.cache import cache

from .models import Order, OrderItem , VazvratProdcut , CategoryProduct , Cupon , ContactForm
from config.settings import site_name



class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"

class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = "__all__"


def doller_funtion():
    doller = cache.get_or_set('doller', OrderSetting.objects.first().get_doller_funtion, timeout=60*15)
    return doller

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"



class VazvratProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = VazvratProdcut
        fields =("id", "vazvrat_product")



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"



class OrderGetSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    mahsul0t_narxi = serializers.SerializerMethodField()
    mahsulot_nomi = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = "__all__"


    def get_mahsulot_nomi(self, obj):
        return obj.product.product_name

    def get_mahsul0t_narxi(self, obj):
        if obj.mahsul0t_narxi:
            return obj.mahsul0t_narxi
        else:
            return int(obj.product.price * doller_funtion())

    def get_images(self, obj):
        images = obj.product.images.all()
        if images:
            return [site_name +  image.image.url  for image in images]
        

    def get_price(self, obj):
        if obj.product.price:
            return obj.product.price


class OrderGetUserSerializer(serializers.ModelSerializer):
    order_items = OrderItemProductSerializer(many=True)
    order_obj = serializers.SerializerMethodField(read_only=True)
    status_color = serializers.SerializerMethodField(read_only=True)
    times = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"


    def get_times(self, obj):
        return obj.created_at.strftime("%B %d %Y %H:%M")

    def get_order_obj(self, obj):
        prod_lengs = obj.order_items.count()
        yetkazib_berish_manzili = obj.punkit and obj.punkit.name or (obj.qishloq and obj.qishloq )
        tolov_usuli = obj.tolov_usullar and obj.tolov_usullar.name or ""
        narxi = obj.total_price and obj.total_price or 0 
        yetkazib_berish = obj.dastafka_summa and obj.dastafka_summa or 0 
        status = obj.status and obj.status or ""
        yetkazish_vaqti = obj.yetkazish and obj.yetkazish.strftime("%Y-%m-%d") or (obj.teskor_buyurtma and "90 minut" or 'olib ketish')
        create_at = obj.created_at and obj.created_at.strftime("%Y-%m-%d") 
        cashack_summa = obj.tushadigan_cash_summa and obj.tushadigan_cash_summa or 0
        comment = obj.comment and obj.comment or "-- "
        
        data = {
                "Buyurtma raqami": obj.zakas_id,
                "status": status,
                "Buyurtma vaqti": create_at,
                "Yetkazib berish vaqti": yetkazish_vaqti,
                "Tolov usuli": tolov_usuli,
                "Buyurtma turi": "onliyn",
                "Yetkazib berish manzili": yetkazib_berish_manzili,
                "Sotuvchi Xabari": comment
            }
        if cashack_summa>0:
            data[ "Tushadigan Cashback "] = cashack_summa
        return {"data": data, "summa": {f"{prod_lengs} Mahsulot narxi" : f"{narxi} ", "Yetkazib berish": yetkazib_berish , "Jami summa": int(narxi + yetkazib_berish),}, "message": "buyurtma oqilgan"}
    
    def get_status_color(self, obj):
        status = obj.status and obj.status or ""
        status_color = "blue" if status == "pending" else "green"  
        return status_color


        


