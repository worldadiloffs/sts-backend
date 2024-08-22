from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from .serialziers import SitePageSerialzier , SettingsSeriazlier , PaymentSerialzier , DeliveryServiceSeriazleir
from .models import SitePage , SiteSettings , PaymentMethod , DeliveryService, Shaharlar , Tumanlar


class PageApiviews(APIView):
    def get(self, request):
        site_page = SitePage.objects.filter(status=True, site_sts=True)
        serialzieer = SitePageSerialzier(site_page, many=True)
        return JsonResponse(
            {"data": serialzieer.data, "errors":True, "message": ""}, safe=False
        )
    
class SiteSettingsApiviews(APIView):
    def get(self, request):
        settings_model = SiteSettings.objects.filter(site_sts=True).first()
        setting_serialzier = SettingsSeriazlier(settings_model, many=False)
        payment = PaymentMethod.objects.filter(site_sts=True, status=True)
        payment_serialzier = PaymentSerialzier(payment, many=True)
        site_page = SitePage.objects.filter(status=True, site_sts=True)
        serialzieer = SitePageSerialzier(site_page, many=True)
        delivery =DeliveryService.objects.filter(site_sts=True).first()
        delivery_serialzeir = DeliveryServiceSeriazleir(delivery) 
        return JsonResponse(
            {"data": {
                "settings": setting_serialzier.data,
                "payment": payment_serialzier.data,
                "sitePage":serialzieer.data ,
                "delivery": delivery_serialzeir.data
            }, "errors": False, "message": ""}, safe=False
        )

 
 
    {
      "title": "Toshkent viloyati",
      "shahar": [
        { "name": "Ohangaron tumani" },
        { "name": "Ohangaron shahar" },
        { "name": "Bo'stonliq tumani" },
        { "name": "Quyi Chirchiq tumani" },
        { "name": "Oqqo'rg'on tumani" },
        { "name": "Parkent tumani" },
        { "name": "Piskent tumani" },
        { "name": "O'rta Chirchiq tumani" },
        { "name": "Qibray tumani" },
        { "name": "Yuqori Chirchiq tumani" },
        { "name": "Yangiyo'l tumani" },
        { "name": "Zangiota tumani" },
        { "name": "Chinoz tumani" },
        { "name": "Bekobod tumani" },
        { "name": "Yangibozor shahar" }
      ]
    },


class ShaharLarPostApiviews(APIView):
    def post(self, request):
        data = request.data["data"]
        for i in data:
            shahar = Shaharlar.objects.create(name=i['title'], site_sts=True,site_rts=True)
            shahar.save()
            for j in i['shahar']:
                tuman = Tumanlar.objects.create(name=j['name'], viloyat=shahar)
                tuman.save()
        return JsonResponse({"data": "success", "errors": False, "message": ""}, safe=False)

