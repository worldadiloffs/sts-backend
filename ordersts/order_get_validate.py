from rest_framework.views import APIView
from settings.models import DeliveryService, OrderSetting, PaymentMethod , TolovUsullar , Shaharlar, Tumanlar
from django.http import JsonResponse
from settings.serialziers import DeliveryServiceSeriazleir, DokonSerialzier, ShaharlarSerialzier, TolovUsullarSerialzier, TumanlarSerialzier



class OrderValudeView(APIView):
    def get(self, request):
        delivery = DeliveryService.objects.all()
        payment = PaymentMethod.objects.all()
        tolov = TolovUsullar.objects.all()
        shaharlar = Shaharlar.objects.all()
        tumanlar = Tumanlar.objects.all()
        delivery_serial = DeliveryServiceSeriazleir(delivery, many=True)
        payment_serial = TolovUsullarSerialzier(payment, many=True)
        tolov_serial = TolovUsullarSerialzier(tolov, many=True)
        shaharlar_serial = ShaharlarSerialzier(shaharlar, many=True)
        tumanlar_serial = TumanlarSerialzier(tumanlar, many=True)
        return JsonResponse(
            {
              "data": { "delivery": delivery_serial.data,
                "payment": payment_serial.data,
                "tolov": tolov_serial.data,
                "shaharlar": shaharlar_serial.data,
                "tumanlar": tumanlar_serial.data},
                "errors": False,
                "message": "ok"
              

            }, safe=False)


