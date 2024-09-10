from product.models import Product
from importdata.models import ImportProduct


def run():
    for i in ImportProduct.objects.all():
        if i.quantity > 10:
            i.quantity  = 10
        product = Product()
        product.product_name = i.name
        product.articul = i.articul
        product.price = 1
        product.counts = i.quantity
        product.material_nomer = i.material_nomer 
        product.save()
