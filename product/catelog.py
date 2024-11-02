from multiprocessing import Manager, Process
from django.db import connection
from product.serialzier import ProductListMiniSerilizers  # Serializer joylashgan joyini import qiling
from product.models import MainCategory, Product  # Model joylashgan joyini import qiling
class ProductFetcher:
    def __init__(self, super_id):
        self.super_id = super_id
        self.result = []

    def fetch_products(self):
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
        
        # Natijani saqlash
        self.result = product_object

        # Database connectionni yopish
        connection.close()

    def get_result(self):
        return self.result