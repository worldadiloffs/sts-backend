from rest_framework.views import APIView
from rest_framework.response import Response
from .models  import (JopServis, AboutServis, PriceServis, UstanofkaServis, KomandaServis, CategoryServis, LisenceServis, SavolJavobServis)


from .serialzier import ( JopServisSerializer  , AboutServisSerializer, PriceServisSerializer, UstanofkaServisSerializer, KomandaServis  , CategoryServisSerializer , LisenceServisSerializer, KomandaServisSerializer, SavolJavobServisSerializer)




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
        return Response({
            "jop_servis": jop_servis_serializer.data,
            "about_servis": about_servis_serializer.data,
            "price_servis": price_servis_serializer.data,
            "ustanofka_servis": ustanofka_servis_serializer.data,
            "komanda_servis": komanda_servis_serializer.data,
            "category_servis": category_servis_serializer.data,
            "lisence_servis": lisence_servis_serializer.data,
            "savol_javob": savol_javob_serializer.data
            }, status=200)
    
    
