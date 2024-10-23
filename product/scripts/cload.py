from home.models import Banner
from product.servisses import upload_image_to_cloudflare
from product.models import Image


# def run():
#     homes = Banner.objects.all()
#     for home in homes:
#         if home.image:
#             cload_id = upload_image_to_cloudflare(home.image.file)
#             home.cloudflare_id = cload_id
#             home.save()
#             print(home.cloudflare_id)


def run():
    image = Image.objects.all()[899:1000]
    for i in image:
        if i.image is not None:
            cload_id = upload_image_to_cloudflare(i.image.file)
            i.cloudflare_id = cload_id
            i.save()
            print(i.cloudflare_id)

