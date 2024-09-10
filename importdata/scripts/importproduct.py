from product.models import Product
from importdata.models import ImportProduct


def run():
    for i in ImportProduct.objects.all():
        product = Product()
        product.product_name = i.name
        product.articul = i.articul
        product.price = 1
        product.material_nomer = i.material_nomer
        product.site_sts = True
        product.save()

