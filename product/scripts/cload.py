from home.models import Banner
from product.servisses import upload_image_to_cloudflare
from product.models import Image
from category.models import SuperCategory, MainCategory, SubCategory
from home.models import HomePageCategory , CardImage

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

# def run():
#     j = 0
#     main_category = SubCategory.objects.all()
#     for i in main_category:
#         if i.sub_image:
#             j = j+1
#             i.save()
#             print(j)
#             print(i.cloudflare_id)

def run():
    j = 0
    main_category = HomePageCategory.objects.all()
    for i in main_category:
        if i.image:
            j = j+1
            i.save()
            print(j)
            print(i.cloudflare_id)


