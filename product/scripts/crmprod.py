import requests
from product.models import Product
from random import randint, randrange, Random, random
import string

string.ascii_letters
"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
import random

random.choice(string.ascii_letters)


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for x in range(y))


# print (random_char(5))


# print(randint(10000000, 99999999))
def save_meth():
    data = []
    for i in range(20):
        data.append(f"{random_char(2)}{randint(100000, 200000)}")
    return data


def run():
    product = Product.objects.filter(site_sts=True)[:100]
    for i in product:
        if i.material_nomer is not None:
            serena = True
            product_serena = save_meth()
            product_count = None

        else:
            serena = False
            product_serena = None
            product_count = randint(1, 100)
        req = {
            "product_name": i.product_name,
            "articul": i.articul,
            "price": i.price,
            "counts": i.counts,
            "material_nomer": i.material_nomer,
            "serenaTrue_countFalse": serena,
            "cloud_id": i.cloud_id,
            "product_count": product_count,
            "product_serena": product_serena,
        }
        response = requests.post('https://hikvision-shop.uz/crm/product-data/', json=req)
        if response.status_code == 200:
            print(response.json())
            print(f"Product {i.product_name} saved successfully.")