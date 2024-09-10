from product.models import Product
from .models import ImportProduct



for i in ImportProduct.objects.all():
    product = Product()
    product.product_name = i.name
    product.articul = i.articul
    product.price = 1
    product.material_nomer = i.material_nomer 
    product.save()