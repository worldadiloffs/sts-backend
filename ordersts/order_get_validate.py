from rest_framework.views import APIView
from settings.models import DeliveryService, MuddatliTolovxizmatlar, OrderSetting, PaymentMethod , TolovUsullar , Shaharlar, Tumanlar, Dokon
from django.http import JsonResponse
from settings.serialziers import DeliveryServiceSeriazleir, DokonSerialzier, ShaharlarSerialzier, TolovUsullarSerialzier, TumanlarSerialzier

from django.utils import timezone

from datetime import datetime
from django.utils.timezone import activate
from config.settings import site_name




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
    




class MuddatliTOlovOrderView(APIView):
     def post(self, request):
            muddat_tolov = []
            price = request.data.get('price')
            if price is not None:
                if (MuddatliTolovxizmatlar.objects.count() > 0):
                    for i in MuddatliTolovxizmatlar.objects.all():
                        muddat_tolov.append({
                        "logo": i.logo and ( site_name +  i.logo.url) or None,
                        "name": i.name,
                        "oylar": i.kredit(price)})
                    
                    return JsonResponse(
                        {
                        "data": muddat_tolov,
                        "errors": False,
                        "message": "ok"}, safe=False)
                return JsonResponse({"data": None, "errors": True, "message": "Muddatli tolov mavjud emas"}, safe=False)
                
            else:
                return JsonResponse(
                    {"data": None, "errors": True, "message": "Muddatli tolov qator bo'ladi"}, safe=False)
            




class DastafkaOrderView(APIView):
     def post(self, request):
        summa = request.data.get('summa')
        viloyat_id = request.data.get('viloyat_id')
        res_summa = None
        if viloyat_id is None:
            return JsonResponse(
                   {"data": None, "errors": True, "message": "Viloyat id bo'ladi"}, safe=False)
        yetkazib_berish_turi = request.data.get('yetkazib_berish_turi')
        if yetkazib_berish_turi is None:
            shahar = Shaharlar.objects.get(id=viloyat_id)
            if shahar.zakas_summa is not None:
                if summa >= shahar.zakas_summa:
                    res_summa = summa 
                else:
                    res_summa = summa + shahar.summa
            if shahar.zakas_summa is None:
                res_summa = summa
        if yetkazib_berish_turi == 'teskor':
            deliver  = DeliveryService.objects.filter(site_sts=True).first()
            if summa >=deliver.zakas_summa:
                res_summa = summa
            res_summa =  summa + deliver.dastafka_summa
        
        if yetkazib_berish_turi =='standart':
            shahar = Shaharlar.objects.get(id=viloyat_id)
            if shahar.zakas_summa is not None:
                if summa >= shahar.zakas_summa:
                    res_summa = summa 
                else:
                    res_summa = summa + shahar.summa
            if shahar.zakas_summa is None:
                res_summa = summa

        if res_summa is  None:
            return JsonResponse({"summa": summa , "message": "ok"}, safe=False)
        return JsonResponse({"summa": res_summa , "message": "ok"}, safe=False)
           
          
       
          
  

