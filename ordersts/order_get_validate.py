from rest_framework.views import APIView
from settings.models import DeliveryService, MuddatliTolovxizmatlar,  TolovUsullar , Shaharlar,  Dokon
from django.http import JsonResponse
from settings.serialziers import DeliveryServiceSeriazleir, DokonSerialzier, ShaharlarSerialzier, TolovUsullarSerialzier
from config.settings import site_name




class OrderValudeView(APIView):
    def get(self, request, site):
        if site == 'sts':    
            delivery = DeliveryService.objects.filter(site_sts=True).first()
            tolov = TolovUsullar.objects.filter(site_sts=True)
            dokon = Dokon.objects.filter(site_sts=True)
        if site == 'rts':
            delivery = DeliveryService.objects.filter(site_rts=True).first()
            tolov = TolovUsullar.objects.filter(site_rts=True)
            dokon = Dokon.objects.filter(site_rts=True)
        shaharlar = Shaharlar.objects.all()
        delivery_serial = DeliveryServiceSeriazleir(delivery)
        tolov_serial = TolovUsullarSerialzier(tolov, many=True)
        shaharlar_serial = ShaharlarSerialzier(shaharlar, many=True)
        dokon_serial = DokonSerialzier(dokon, many=True)
        return JsonResponse(
            {
              "data": { 
                "delivery": delivery_serial.data,
                "tolov": tolov_serial.data,
                "shaharlar": shaharlar_serial.data,
                "dokonlar": dokon_serial.data
                },
                "errors": False,
                "message": "ok"
              

            }, safe=False)
    




class MuddatliTOlovOrderView(APIView):
     def post(self, request, site):
            muddat_tolov = []
            price = request.data.get('price')
            if price is not None:
                if (MuddatliTolovxizmatlar.objects.count() > 0):
                    if site == 'sts':
                        muddat = MuddatliTolovxizmatlar.objects.filter(site_sts=True, status=True)

                    if site == 'rts':
                        muddat = MuddatliTolovxizmatlar.objects.filter(site_rts=True, status=True)
                    for i in muddat:
                        muddat_tolov.append({
                        "logo": i.logo and ( site_name +  i.logo.url) or None,
                        "name": i.name,
                        "oylar": i.kredit(price)})
                    
                    return JsonResponse(
                        {
                        "data": muddat_tolov,
                        "errors": False,
                        "message": "ok"}, safe=False, status=200)
                return JsonResponse({"data": None, "errors": True, "message": "Muddatli tolov mavjud emas"}, safe=False, status=400)
                
            else:
                return JsonResponse(
                    {"data": None, "errors": True, "message": "Muddatli tolov qator bo'ladi"}, safe=False, status=400)
            




class DastafkaOrderView(APIView):
     def post(self, request, site):
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
                    res_summa = 0
                else:
                    res_summa = shahar.summa
            if shahar.zakas_summa is None:
                res_summa = 0
        if str(yetkazib_berish_turi) =='teskor':
            if site == 'sts':
                deliver  = DeliveryService.objects.filter(site_sts=True).first()
            if site == 'rts':
                deliver  = DeliveryService.objects.filter(site_rts=True).first()
            if summa >= deliver.zakas_summa:
                res_summa = 0
            else:
                res_summa =  deliver.dastafka_summa
        
        if str(yetkazib_berish_turi) =='standart':
            shahar = Shaharlar.objects.get(id=viloyat_id)
            if shahar.zakas_summa is not None:
                if summa >= shahar.zakas_summa:
                    res_summa = 0
                else:
                    res_summa = shahar.summa
            if shahar.zakas_summa is None:
                res_summa = shahar.summa

        if res_summa is  None:
            return JsonResponse({"summa": 0 , "message": "ok"}, safe=False, status=200)
        return JsonResponse({"summa": res_summa , "message": "ok"}, safe=False, status=200)
           
          
       
          
  

