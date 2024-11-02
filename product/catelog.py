from multiprocessing import Process
from django.db import connection
from .serialzier import ProductListMiniSerilizers  # Serializer joylashgan joyini import qiling
from .models import MainCategory, Product  # Model joylashgan joyini import qiling

class ProductFetcher:
    def __init__(self, super_ids):
        """
        `super_ids` - bu `superCategory` id'larning ro'yxati bo'lib, 
        har bir jarayonda o'sha kategoriyalar uchun mahsulotlarni olib keladi.
        """
        self.super_ids = super_ids
        self.results = []

    def fetch_products(self, super_id):
        """
        Har bir kategoriya uchun mahsulotlarni olib keluvchi yordamchi metod.
        """
        product_object = []
        for main in MainCategory.objects.filter(superCategory__id=super_id, status=True):
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
        
        # Process tugagandan keyin connectionni yopamiz
        connection.close()
        
        # Natijani saqlaymiz
        self.results.append(product_object)

    def run_processes(self):
        """
        `fetch_products` metodini har bir `super_id` uchun alohida jarayonda ishga tushiradi.
        """
        processes = [
            Process(target=self.fetch_products, args=(super_id,))
            for super_id in self.super_ids
        ]

        # Jarayonlarni boshlash
        for p in processes:
            p.start()

        # Jarayonlar tugashini kutish
        for p in processes:
            p.join()

    def get_results(self):
        """
        `run_processes` tugaganidan so'ng to'plangan natijalarni qaytaradi.
        """
        return self.results
