from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cupon
from .serializers import CuponSerializer
from datetime import date


class CuponApiViews(APIView):
    def get(self, request):
        cupon = Cupon.objects.all()
        serializer = CuponSerializer(cupon, many=True)
        return Response(serializer.data)
    



class CoponPostApiviews(APIView):
    def post(self, request):
        price = request.data.get('price')
        promocod = request.data.get('promocod')

        kun = date.today()
        copon = Cupon.objects.filter(code=promocod, start_date__lte=kun, end_date__gte=kun).first()
        if copon is not None:
            if price >= copon.max_summa:
                return Response({"data": {"summa": copon.summa}, "errrors": False, "message": "ok"})
            return Response({"data": {"summa": 0}, "errors":False , "message": "summa yetarli emas"})
        return Response({"data": None, "errors": True, "message": "Kupon mavjud emas"})
        
