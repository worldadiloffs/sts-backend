from rest_framework.views import APIView
from settings.models import DeliveryService, OrderSetting, PaymentMethod , TolovUsullar , Shaharlar, Tumanlar, Dokon
from django.http import JsonResponse
from settings.serialziers import DeliveryServiceSeriazleir, DokonSerialzier, ShaharlarSerialzier, TolovUsullarSerialzier, TumanlarSerialzier

from django.utils import timezone

from datetime import datetime
from django.utils.timezone import activate




def _teskor_buyurtma_test(request):
    if int(datetime.now().strftime('%H'))>=18:
         return f"{timezone.now() + timezone.timedelta(hours=16)}" 
    if int(timezone.now().strftime('%H'))<6:
        return f"{timezone.now() + timezone.timedelta(hours=16)}"
    if int(timezone.now().strftime('%H'))>14:
              return f"{timezone.now() + timezone.timedelta(hours=6)}" 
               
    if int(timezone.now().strftime('%H'))<14:
        return f"{timezone.now() + timezone.timedelta(hours=6)}" 

class OrderValudeView(APIView):
    def get(self, request):
            
        delivery = DeliveryService.objects.filter(site_sts=True).first()
        if delivery.teskor_buyurtma:
             teskor_buyurtma_date = _teskor_buyurtma_test(request=request)

        else:
             teskor_buyurtma_date = None
        tolov = TolovUsullar.objects.filter(site_sts=True)
        shaharlar = Shaharlar.objects.all()
        dokon = Dokon.objects.filter(site_sts=True)
        delivery_serial = DeliveryServiceSeriazleir(delivery)
        tolov_serial = TolovUsullarSerialzier(tolov, many=True)
        shaharlar_serial = ShaharlarSerialzier(shaharlar, many=True)
        dokon_serial = DokonSerialzier(dokon, many=True)
        return JsonResponse(
            {
              "data": { 
                "delivery": delivery_serial.data,
                "teskor_buyurtma_date" : teskor_buyurtma_date,
                "tolov": tolov_serial.data,
                "shaharlar": shaharlar_serial.data,
                "dokonlar": dokon_serial.data
                },
                "errors": False,
                "message": "ok"
              

            }, safe=False)


