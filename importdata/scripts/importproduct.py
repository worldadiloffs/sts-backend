from product.models import Product
from importdata.models import ImportProduct


def run():
    for i in ImportProduct.objects.all():
        if i.name is not None:
            materila_bool = Product.objects.filter(material_nomer=i.material_nomer).exists()
            articul_bool = Product.objects.filter(articul=i.articul).exists()
            if not(materila_bool) and not(articul_bool):
                if i.quantity > 10:
                    i.quantity  = 10
                product = Product()
                product.product_name = i.name
                product.articul = i.articul
                product.price = 1
                product.counts = i.quantity
                product.material_nomer = i.material_nomer 
                product.site_sts = True  # site status true
                product.save()
