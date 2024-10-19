from .models import Product


def content_product(request):
    product_status_true = Product.objects.filter(status=True, site_sts=True).count()
    product_rts_status_false = Product.objects.filter(status=True, site_rts=True).count()
    rts__tavarlar = Product.objects.filter(site_rts=True,).count()
    product_count_all = Product.objects.filter(site_sts=True).count()

    return {"product_status_true": product_status_true,  "product_count_all": product_count_all , "rts_tavarlar_active": product_rts_status_false , "rts_tavarlar":rts__tavarlar}