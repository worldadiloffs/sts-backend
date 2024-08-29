from rest_framework import serializers

from settings.models import OrderSetting

from .models import Order, OrderItem
from config.settings import site_name
def doller_funtion():
    order = OrderSetting.objects.first()
    return order.doller * 1.12 # 1.12 is for dollar exchange rate

class OrderItemSerializer(serializers.ModelSerializer):
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
    status_color = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

    def get_order_obj(self, obj):
        prod_lengs = obj.order_items.count()
        yetkazib_berish_manzili = obj.punkit and obj.punkit.name or (obj.qishloq and obj.qishloq or "FIrma orqali buyurtma")
        tolov_usuli = obj.tolov_usullar and obj.tolov_usullar.name or ""
        narxi = obj.total_price and obj.total_price or 0 
        yetkazib_berish = obj.dastafka_summa and obj.dastafka_summa or 0 
        status = obj.status and obj.status or ""
        yetkazish_vaqti = obj.yetkazish and obj.yetkazish.strftime("%Y-%m-%d") or "90 minutov"
        create_at = obj.created_at and obj.created_at.strftime("%Y-%m-%d") 
        data = {
            "Buyurtma raqami": obj.zakas_id,
            "status": status,
            "Buyurtma vaqti": create_at,
            "Yetkazib berish vaqti": yetkazish_vaqti,
            "Tolov usuli": tolov_usuli,
            "Buyurtma turi": "onliyn",
            "Yetkazib berish manzili": yetkazib_berish_manzili,
        }
        return {"data": data, "summa": {f"{prod_lengs} Mahsulot narxi" : f"{narxi} so'm", "Yetkazib berish": f"{format(yetkazib_berish)} so'm" , "Jami summa": f"{format(int(narxi + yetkazib_berish))} so'm", "message": "buyurtma oqilgan"}}
    
    def get_status_color(self, obj):
        status = obj.status and obj.status or ""
        status_color = "blue" if status == "pending" else "green"
        return status_color


        


