from rest_framework.views import APIView 
from product.models import Product
from rest_framework.response import Response
#    product.product_name = i.name
#         product.articul = i.articul
#         product.price = 1
#         product.counts = i.quantity
#         product.material_nomer = i.material_nomer 

class ProductImportApiviews(APIView):
    def post(self, request):
        name = request.data.get('name')
        articul = request.data.get('articul')
        counts = request.data.get('quantity')
        material_nomer = request.data.get('material_nomer')
        if int(counts) >10:
            counts = 10
        if name is not None:
            product = Product()
            product.product_name = name
            product.articul = articul
            product.price = 1
            product.counts = counts
            product.material_nomer = material_nomer
            product.save()
            return Response({'message': 'Product created successfully'}, status=201)
        

