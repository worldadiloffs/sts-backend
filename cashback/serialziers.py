from rest_framework import serializers
from .models import CashbackKard

class CashbackKardSerializer(serializers.ModelSerializer):
    hisobot = serializers.SerializerMethodField()
    class Meta:
        model = CashbackKard
        fields = "__all__"



# {"zakas_id": self.zakas_id, "summa": self.tushadigan_cash_summa, "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') , "hisob": "+"}

    def get_hisobot(self, obj):
        create_at = obj.create_date and obj.create_date.strftime("%Y-%m-%d") 

        hisobot_ob = obj.hisobot
        data = []
        if hisobot_ob:
            for i in hisobot_ob:
                data.append({
                    "Buyurtma raqami": i['zakas_id'],
                    "Summa": f"{i['summa']}",
                    "Mahsulotni Buyurtma  vaqt": create_at,
                    "Hisob": i['hisob']
                })
            return data
        return None
            


class CashbackMobileSerialziers(serializers.ModelSerializer):
    class Meta:
        model = CashbackKard
        fields = "__all__"
            




    