from product.models import Product
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from product.serialzier import CalculatorProdcutSerialzier





class ProductSearchCalculatorView(APIView):
    def get(self, request, site):
        search = request.GET.get("search", "")
        if search:
            if site == 'sts':
                products = Product.objects.filter(site_sts=True).filter(
                    Q(product_name__icontains=search) 
                )[:10]
            if site == 'rts':
                products = Product.objects.filter(site_sts=True).filter(
                    Q(name__icontains=search) 
                )[:10]

            product_serialzier = CalculatorProdcutSerialzier(products, many=True)

            return Response(product_serialzier.data)
        return Response({"Поиск не дал результатов" :0})
    