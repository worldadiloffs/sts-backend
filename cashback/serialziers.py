from rest_framework import serializers
from .models import CashbackKard

class CashbackKardSerializer(serializers.ModelSerializer):
    hisobot_ob = serializers.SerializerMethodField()
    class Meta:
        model = CashbackKard
        fields = "__all__"



# {"zakas_id": self.zakas_id, "summa": self.tushadigan_cash_summa, "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') , "hisob": "+"}

    def get_hisobot_ob(self, obj):
        hisobot_ob = obj.hisobot
        data = []
        if hisobot_ob:
            for i in hisobot_ob:
                data.append({
                    "Buyurtma raqami": i['zakas_id'],
                    "Summa": f"{i['summa']} so'm ",
                    "Mahsulotni Buyurtma qilingan vaqt": i['created_at'],
                    "Hisob": i['hisob']
                })
            return data
        return None
            

            


    