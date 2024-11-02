from multiprocessing import Process
from django.db import connection
from product.serialzier import ProductListMiniSerilizers  # Serializer joylashgan joyini import qiling
from product.models import MainCategory, Product  # Model joylashgan joyini import qiling

class ProductFetcher:
    def __init__(self, super_id):
        """
        `super_id` - bu bitta `superCategory` id bo'lib, o'sha kategoriya uchun mahsulotlarni olib keladi.
        """
        self.super_id = super_id
        self.result = []

    def fetch_products(self):
        """
        Kategoriyaga mos mahsulotlarni olib keluvchi yordamchi metod.
        """
        product_object = []
        for main in MainCategory.objects.filter(superCategory__id=self.super_id, status=True):
            prod_obj = Product.objects.select_related('main_category').filter(
                status=True, main_category__id=main.pk
            )[:5]
            serializer = ProductListMiniSerilizers(prod_obj, many=True)
            if prod_obj:
                sub_names = main.main_content if main.main_content else main.main_name
                data = {
                    "category": sub_names,
                    "product": serializer.data,
                }
                product_object.append(data)
        
        # Natijani saqlaymiz
        self.result = product_object

        # Process tugagandan keyin connectionni yopamiz
        connection.close()

    def run_process(self):
        """
        `fetch_products` metodini bitta jarayonda ishga tushiradi.
        """
        process = Process(target=self.fetch_products)
        
        # Jarayonni boshlash
        process.start()

        # Jarayon tugashini kutish
        process.join()

    def get_result(self):
        """
        `run_process` tugaganidan so'ng to'plangan natijalarni qaytaradi.
        """
        return self.result