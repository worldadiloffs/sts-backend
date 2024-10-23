from product.models import Product , Image as ImagesObj
from PIL import Image
from io import BytesIO
from django.core.files import File

def run():
    for i in ImagesObj.objects.all()[:100]:
        # Rasmni o'qish
        if i.image:
            img = Image.open(i.image)

            # Agar format webp bo'lsa
            if img.format.lower() == 'webp':
                img = img.convert('RGB')  # webp ni jpg formatiga mos ravishda o'zgartirish

                # Faylni o'zgartirish
                img_io = BytesIO()
                img.save(img_io, format='JPEG')

                # Eski faylni yangi fayl bilan almashtirish
                new_image = File(img_io, name=i.image.name.replace('webp', 'jpg'))
                i.image.save(new_image.name, new_image, save=False)
        print(i.product)


# def run():
#     counts = ImagesObj.objects.count()
#     print(f"Image count: {counts}")



