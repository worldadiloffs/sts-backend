

from django.http import JsonResponse
from .models import MainCategory, SubCategory

def get_main_categories(request):
    if request.method == 'GET':
        super_category_id = request.GET.get('super_category')
        main_categories = MainCategory.objects.filter(superCategory_id=super_category_id)
        data = [{'id': cat.pk, 'name': cat.main_name} for cat in main_categories]
        return JsonResponse(data, safe=False)

def get_sub_categories(request):
    if request.method == 'GET':
        main_category_id = request.GET.get('main_category')
        sub_categories = SubCategory.objects.filter(mainCategory_id=main_category_id)
        data = [{'id': cat.pk, 'name': cat.sub_name} for cat in sub_categories]
        return JsonResponse(data, safe=False)