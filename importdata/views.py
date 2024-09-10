from rest_framework.views import APIView 
from product.models import Product
from product.serialzier import ProductListMiniSerilizers
from rest_framework.response import Response
from .models import ImportProduct
from .serialziers import ImportProdcutSerialzeirs
import requests
#    product.product_name = i.name
#         product.articul = i.articul
#         product.price = 1
#         product.counts = i.quantity
#         product.material_nomer = i.material_nomer 

class ProductImportApiviews(APIView):
    def post(self, request):
        data = request.data
        for i in data:
            name = i.get('name')
            articul = i.get('articul')
            counts = i.get('quantity')
            material_nomer = i.get('material_nomer')
            articuls:bool = Product.objects.filter(articul=articul).exists()
            materila_nomer:bool=  Product.objects.filter(material_nomer=material_nomer).exists()
            if not(articuls) and not(materila_nomer):
                if int(counts) >10:
                        counts = 10
                if name is not None:
                    product = Product()
                    product.product_name = name
                    product.articul = articul
                    product.price = 1
                    product.counts = counts
                    product.material_nomer = material_nomer
                    product.site_sts = True
                    product.save()
        return Response({'message': 'Product created successfully'}, status=201)
        



class ImportGet(APIView):
    def get(self, request):
        serializer = list(Product.objects.all().order_by("id").values("id", "product_name", "articul", "price", "counts", "slug"))
        return Response({"data": serializer})

        

