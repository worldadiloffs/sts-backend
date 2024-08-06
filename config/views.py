import requests
from django.http import JsonResponse
import json


res = requests.get('https://hikvision-shop.uz/crm/product-data/')
print(res)


def product(request):
    res = requests.get('https://hikvision-shop.uz/crm/product-data/')
    return JsonResponse({"data":res.json() , "errors":False, "message":""}, safe=False) 

    


