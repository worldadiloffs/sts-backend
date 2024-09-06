from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cupon
from .serializers import CuponSerializer


class CuponApiViews(APIView):
    def get(self, request):
        cupon = Cupon.objects.all()
        serializer = CuponSerializer(cupon, many=True)
        return Response(serializer.data)
    

    