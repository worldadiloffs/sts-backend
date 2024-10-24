from home.models import Banner
from product.servisses import upload_image_to_cloudflare
from product.models import Image
from category.models import SuperCategory, MainCategory, SubCategory


# def run():
#     homes = Banner.objects.all()
#     for home in homes:
#         if home.image:
#             cload_id = upload_image_to_cloudflare(home.image.file)
#             home.cloudflare_id = cload_id
#             home.save()
#             print(home.cloudflare_id)


# def run():
#     # count = Image.objects.all().count()
#     # print(count)
#     image = Image.objects.all()[1799:]
#     j = 0
#     for i in image:
#         if i.image is not None:
#             cload_id = upload_image_to_cloudflare(i.image.file)
#             i.cloudflare_id = cload_id
#             i.save()
#             j = j+1 
#             print(j)
#             print(i.cloudflare_id)

def run():
    super_categories = SuperCategory.objects.all()
    for super_category in super_categories:
        if super_category.category_image:
            # cload_id = upload_image_to_cloudflare(super_category.category_image.file)
            # super_category.cloudflare_id = cload_id
            super_category.save()
            print(super_category.cloudflare_id)


