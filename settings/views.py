from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from .serialziers import PageContentSerialzier, SitePageSerialzier , SettingsSeriazlier , PaymentSerialzier , DeliveryServiceSeriazleir , ServisPageSerialzier
from .models import PageContent, SitePage , SiteSettings , PaymentMethod , DeliveryService, Shaharlar , Tumanlar , ServisPage



class ServisPageApiviews(APIView):
    def get(self, request, site):
        if site == 'sts':
            page_content = ServisPage.objects.filter(site_sts=True, status=True).first()
        if site == 'rts':
            page_content = ServisPage.objects.filter(site_rts=True, status=True).first()
        serialzier = ServisPageSerialzier(page_content)
        return JsonResponse(
            {"data": serialzier.data, "errors": True, "message": ""}, safe=False
        )



class PageApiviews(APIView):
    def get(self, request, site):
        if site == 'sts':
            site_page = SitePage.objects.filter(status=True, site_sts=True)
        if site == 'rts':
            site_page = SitePage.objects.filter(status=True, site_rts=True)
        serialzieer = SitePageSerialzier(site_page, many=True)
        return JsonResponse(
            {"data": serialzieer.data, "errors":True, "message": ""}, safe=False
        )
    
class SiteSettingsApiviews(APIView):
    def get(self, request, site):
        if site =='sts':
            settings_model = SiteSettings.objects.filter(site_sts=True).first()
            payment = PaymentMethod.objects.filter(site_sts=True, status=True)
            site_page = SitePage.objects.filter(status=True, site_sts=True)
            delivery =DeliveryService.objects.filter(site_sts=True).first()
        if site == 'rts':
            settings_model = SiteSettings.objects.filter(site_rts=True).first()
            payment = PaymentMethod.objects.filter(site_rts=True, status=True)
            site_page = SitePage.objects.filter(status=True, site_rts=True)
            delivery = DeliveryService.objects.filter(site_rts=True).first()

        setting_serialzier = SettingsSeriazlier(settings_model, many=False)
       
        payment_serialzier = PaymentSerialzier(payment, many=True)
        
        serialzieer = SitePageSerialzier(site_page, many=True)
        delivery_serialzeir = DeliveryServiceSeriazleir(delivery) 
        return JsonResponse(
            {"data": {
                "settings": setting_serialzier.data,
                "payment": payment_serialzier.data,
                "sitePage":serialzieer.data ,
                "delivery": delivery_serialzeir.data
            }, "errors": False, "message": ""}, safe=False
        )
    



class PageContentApiviews(APIView):
    def get(self, request, site, slug):
        if site == 'sts':
            page_content = PageContent.objects.filter(site_sts=True, slug=slug).first()
        if site == 'rts':
            page_content = PageContent.objects.filter(site_rts=True, slug=slug).first()
        serialzier = PageContentSerialzier(page_content)
        return JsonResponse(
            {"data": serialzier.data, "errors": True, "message": ""}, safe=False
        )


class ShaharLarPostApiviews(APIView):
    def post(self, request):
        data = request.data["data"]
        for i in data:
            shahar = Shaharlar()
            shahar.name_uz = i['title']
            shahar.name_ru = i['title_ru']
            shahar.site_sts = True
            shahar.site_rts = True
            shahar.zakas_summa= 1000000
            shahar.summa = 30000
            shahar.dastafka
            shahar.save()
            index = 0
            for j in range(0, (len(i['shahar'])-1)):

                tuman = Tumanlar()
                tuman.name_uz = i['shahar'][j]['name']
                tuman.name_ru = i['shahar_ru'][j]['name']
                tuman.viloyat = shahar
                tuman.save()
        return JsonResponse({"data": "success", "errors": False, "message": ""}, safe=False)
