from rest_framework.views import APIView
from rest_framework.response import Response
from .models  import (JopServis, AboutServis, KontaktServis, PriceServis, UstanofkaServis, KomandaServis, CategoryServis, LisenceServis, SavolJavobServis, ContactContentServis)


from .serialzier import ( JopServisSerializer  , AboutServisSerializer, KontaktServisSerializer, PriceServisSerializer, UstanofkaServisSerializer, KomandaServis  , CategoryServisSerializer , LisenceServisSerializer, KomandaServisSerializer, SavolJavobServisSerializer , ContactContentServisSerializer)


from account.send_otp import send_otp
from rest_framework import status


from extensions.code_generator import get_client_ip
from django.core.cache import cache

class HomePageViewsOne(APIView):
    def get(self, request):
        jop_servis = JopServis.objects.first()
        jop_servis_serializer = JopServisSerializer(jop_servis)
        about_servis = AboutServis.objects.first()
        about_servis_serializer = AboutServisSerializer(about_servis)
        price_servis = PriceServis.objects.first()
        price_servis_serializer = PriceServisSerializer(price_servis)
        ustanofka_servis = UstanofkaServis.objects.first()
        ustanofka_servis_serializer = UstanofkaServisSerializer(ustanofka_servis)
        komanda_servis = KomandaServis.objects.first()
        komanda_servis_serializer = KomandaServisSerializer(komanda_servis)
        category_servis = CategoryServis.objects.first()
        category_servis_serializer = CategoryServisSerializer(category_servis)
        lisence_servis = LisenceServis.objects.first()
        lisence_servis_serializer = LisenceServisSerializer(lisence_servis)
        savol_javob = SavolJavobServis.objects.filter(status=True)
        savol_javob_serializer = SavolJavobServisSerializer(savol_javob, many=True)
        contact_content = ContactContentServis.objects.first()
        contact_content_serializer = ContactContentServisSerializer(contact_content)
        return Response({
            "contact_content": contact_content_serializer.data,
            "jop_servis": jop_servis_serializer.data,
            "about_servis": about_servis_serializer.data,
            "price_servis": price_servis_serializer.data,
            "ustanofka_servis": ustanofka_servis_serializer.data,
            "komanda_servis": komanda_servis_serializer.data,
            "category_servis": category_servis_serializer.data,
            "lisence_servis": lisence_servis_serializer.data,
            "savol_javob": savol_javob_serializer.data
            }, status=200)


class ContactformApiView(APIView):
    # throttle_scope = "verify_authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]
    def post(self, request):
        phone = request.data.get('phone')
        if phone is not None:
            return send_otp(request, phone, status=status.HTTP_200_OK)
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        contact = KontaktServis.objects.all()
        serializer = KontaktServisSerializer(contact, many=True)
        return Response(serializer.data, status=200)
    


class VerifyphoneApiView(APIView):
    # throttle_scope = "verify_authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]
    def post(self, request):
        received_code = request.data.get('code')
        phone = request.data.get('phone')
        client_status = request.data.get('status')
        if received_code is not None:
            ip = get_client_ip(request)
            phone = cache.get(f"{ip}-for-authentication")
            otp = cache.get(phone)
            if otp == received_code:
                cache.delete(f"{ip}-for-authentication")
                cache.delete(phone)
                contact = KontaktServis()
                contact.phone_number = phone
                contact.location = request.data.get('location')
                contact.position = request.data.get('position')
                contact.save()
                return Response({"message": "Success"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "code  is required"}, status=status.HTTP_400_BAD_REQUEST)
    




{
    "phone": "+998912345678",
    "code": "12345",
    "location": "Tashkent",
    "position": ""
}

