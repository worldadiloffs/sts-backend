from rest_framework.views import APIView
from settings.models import DeliveryService, OrderSetting, PaymentMethod , TolovUsullar , Shaharlar, Tumanlar, Dokon
from django.http import JsonResponse
from settings.serialziers import DeliveryServiceSeriazleir, DokonSerialzier, ShaharlarSerialzier, TolovUsullarSerialzier, TumanlarSerialzier

from django.utils import timezone

class OrderValudeView(APIView):
    def get(self, request):
            
        delivery = DeliveryService.objects.all().first()
        # if delivery.teskor_buyurtma:
        #     if int(timezone.datetime.hour)>14:
        #         delivery.teskor_buyurtma_date.hour = 10
        #         delivery.teskor_buyurtma_date.minute = 0
        #         delivery.teskor_buyurtma_date.second = 0
        #         delivery.save()
        #     if int(timezone.datetime.hour)<14:
        #         delivery.teskor_buyurtma_date.hour = 18
        #         delivery.teskor_buyurtma_date.minute = 0
        #         delivery.teskor_buyurtma_date.second = 0
        #         delivery.save()
                
                
            

        tolov = TolovUsullar.objects.all()
        shaharlar = Shaharlar.objects.all()
        dokon = Dokon.objects.all()
        delivery_serial = DeliveryServiceSeriazleir(delivery)
        tolov_serial = TolovUsullarSerialzier(tolov, many=True)
        shaharlar_serial = ShaharlarSerialzier(shaharlar, many=True)
        dokon_serial = DokonSerialzier(dokon, many=True)
        return JsonResponse(
            {
              "data": { "delivery": delivery_serial.data,
                "tolov": tolov_serial.data,
                "shaharlar": shaharlar_serial.data,
                "dokonlar": dokon_serial.data
                },
                "errors": False,
                "message": "ok"
              

            }, safe=False)


