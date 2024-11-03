import requests
from product.models import Product


def run():
    product = Product.objects.filter(site_sts=True)[:100]
    for i in product:
        if i.material_nomer is not None:
            serena = True
        else:
            serena = False
        req = {
            "product_name": i.product_name,
            "articul": i.articul,
            "price": i.price,
            "counts": i.counts,
            "material_nomer": i.material_nomer,
            "serenaTrue_countFalse": serena,
            "cloud_id": i.cloud_id,
        }
        response = requests.post('https://hikvision-shop.uz/crm/product-data/', json=req)
        if response.status_code == 200:
            print(f"Product {i.product_name} saved successfully.")