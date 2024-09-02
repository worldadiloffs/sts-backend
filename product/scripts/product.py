

from category.models import MainCategory, SubCategory, SuperCategory
from product.models import Product




def run(main_id=2):
    data = []
    for i in range(1, 13):
        filter_super_category = MainCategory.objects.get(id=main_id).superCategory.pk
        main_obj = MainCategory.objects.select_related('superCategory').filter(superCategory__id=filter_super_category)
        for i in main_obj:
            sub_category = SubCategory.objects.select_related("mainCategory").filter(mainCategory__id=i.pk)
            if sub_category is not None:
                for sub in sub_category:
                    prod_count = Product.objects.select_related("sub_category").filter(sub_category__id=sub.pk).count()
                    data.append(
                        {
                            "sub_name": sub.sub_name,
                            "counts": prod_count,
                            "slug": sub.slug,
                            "pk": sub.pk,
                        }
                    )
                    if len(data) > 12:
                        return data
            

