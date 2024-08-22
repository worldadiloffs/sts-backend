from rest_framework.views import APIView
from settings.models import DeliveryService, OrderSetting, PaymentMethod , TolovUsullar , Shaharlar, Tumanlar, Dokon
from django.http import JsonResponse
from settings.serialziers import DeliveryServiceSeriazleir, DokonSerialzier, ShaharlarSerialzier, TolovUsullarSerialzier, TumanlarSerialzier



class OrderValudeView(APIView):
    def get(self, request):
        delivery = DeliveryService.objects.all()
        tolov = TolovUsullar.objects.all()
        shaharlar = Shaharlar.objects.all()
        tumanlar = Tumanlar.objects.all()
        dokon = Dokon.objects.all()
        delivery_serial = DeliveryServiceSeriazleir(delivery, many=True)
        tolov_serial = TolovUsullarSerialzier(tolov, many=True)
        shaharlar_serial = ShaharlarSerialzier(shaharlar, many=True)
        tumanlar_serial = TumanlarSerialzier(tumanlar, many=True)
        dokon_serial = DokonSerialzier(dokon, many=True)
        return JsonResponse(
            {
              "data": { "delivery": delivery_serial.data,
                "tolov": tolov_serial.data,
                "shaharlar": shaharlar_serial.data,
                "tumanlar": tumanlar_serial.data,
                "dokonlar": dokon_serial.data
                },
                "errors": False,
                "message": "ok"
              

            }, safe=False)


