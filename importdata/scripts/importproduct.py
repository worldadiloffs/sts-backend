from product.models import Product
from importdata.models import ImportProduct , PriceUpdate


# def run():
#     for i in ImportProduct.objects.all()[1875:]:
#         if i.name is not None:
#             materila_bool = Product.objects.filter(material_nomer=i.material_nomer).exists()
#             articul_bool = Product.objects.filter(articul=i.articul).exists()
#             if not(materila_bool) and not(articul_bool):
#                 product = Product()
#                 product.product_name = i.name
#                 product.articul = i.articul
#                 product.price = 1
#                 product.counts = i.quantity
#                 product.material_nomer = i.material_nomer 
#                 product.site_rts = True  # site status true
#                 product.save()


# def run():
#     impor_prod = ImportProduct.objects.all()
#     impor_prod.delete()
#     prices = PriceUpdate.objects.all()
#     prices.delete()


# def run():
#     for i in PriceUpdate.objects.all():
#         if i.articul is not None:
#             product = Product.objects.filter(articul=i.articul).first()
#             if product:
#                 product.price = i.price
#                 product.counts = i.quantity
#                 product.save()


def run():
    for i in Product.objects.all():
        if i.price is None:
            i.price * 1.1 
            i.save()