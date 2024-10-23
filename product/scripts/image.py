from product.models import Product , Image as ImagesObj
from category.models import SubCategory, SuperCategory, MainCategory
from PIL import Image
from io import BytesIO
from django.core.files import File

def run():
    for i in MainCategory.objects.all():
        # Rasmni o'qish
        if i.main_image:
            img = Image.open(i.main_image)

            # Agar format webp bo'lsa
            if img.format.lower() == 'webp':
                img = img.convert('RGB')  # webp ni jpg formatiga mos ravishda o'zgartirish

                # Faylni o'zgartirish
                img_io = BytesIO()
                img.save(img_io, format='JPEG')

                # Eski faylni yangi fayl bilan almashtirish
                new_image = File(img_io, name=i.main_image.name.replace('webp', 'jpg'))
                i.main_image.save(new_image.name, new_image, save=False)
                i.save()

                print(i.main_name)


# def run():
#     counts = ImagesObj.objects.count()
#     print(f"Image count: {counts}")



