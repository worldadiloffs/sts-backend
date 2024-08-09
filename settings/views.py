from django.shortcuts import render
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from .serialziers import SitePageSerialzier , SettingsSeriazlier , PaymentSerialzier , DeliveryServiceSeriazleir
from .models import SitePage , SiteSettings , PaymentMethod , DeliveryService


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



