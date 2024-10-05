

from category.models import MainCategory, SubCategory, SuperCategory
from product.models import Product




# def run():
#     product = Product.objects.filter(site_sts=True)
#     image_count = 0
#     content = 0
#     category_count = 0
#     for i in product:
#         if i.short_description is not None:
#             content += 1
#         if i.image is not None:
#             image_count += 1
#         if i.super_category is not None and i.main_category is not None:
#             category_count +=1
#     print("image count: ", image_count)
#     print("content count: ", content)
#     print("category count: ", category_count)

    # prod = Product.objects.filter(site_rts=True,price=1).count()
    # print(prod)

def run():
    for i in Product.objects.all():
        product = Product.objects.get(id=i.id)
        product.price = round(product.price, 3)
        product.save()
        print(product.price)

# STS uchun 
# Tavarlar soni : 1101
# Tavarlar qo'shilgan rasmlar:  475 
# Tavarlar uchun  content : 7 

# RTS uchun 
# Tavarlar soni : 6647
# Tavarlar qo'shilgan rasmlar:  0
# Tavarlar uchun  content : 0




