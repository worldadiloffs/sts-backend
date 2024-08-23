from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from .serialziers import SitePageSerialzier , SettingsSeriazlier , PaymentSerialzier , DeliveryServiceSeriazleir
from .models import SitePage , SiteSettings , PaymentMethod , DeliveryService, Shaharlar , Tumanlar


class RTSPageApiviews(APIView):
    def get(self, request):
        site_page = SitePage.objects.filter(status=True, site_sts=True)
        serialzieer = SitePageSerialzier(site_page, many=True)
        return JsonResponse(
            {"data": serialzieer.data, "errors":True, "message": ""}, safe=False
        )
    
class RTSSiteSettingsApiviews(APIView):
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

# class ShaharLarPostApiviews(APIView):
#     def post(self, request):
#         data = request.data["data"]
#         for i in data:
#             shahar = Shaharlar()
#             shahar.name_uz = i['title']
#             shahar.name_ru = i['title_ru']
#             shahar.site_sts = True
#             shahar.site_rts = True
#             shahar.save()
#             index = 0
#             for j in range(0, (len(i['shahar'])-1)):

#                 tuman = Tumanlar()
#                 tuman.name_uz = i['shahar'][j]['name']
#                 tuman.name_ru = i['shahar_ru'][j]['name']
#                 tuman.viloyat = shahar
#                 tuman.save()
#         return JsonResponse({"data": "success", "errors": False, "message": ""}, safe=False)
