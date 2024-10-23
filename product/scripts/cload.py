from home.models import Banner
from product.servisses import upload_image_to_cloudflare


def run():
    homes = Banner.objects.all()
    for home in homes:
        cload_id = upload_image_to_cloudflare(home.image.file)
        home.cloudflare_id = cload_id
        home.save()
        print(home.cloudflare_id)

