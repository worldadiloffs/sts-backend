


from product.catelog import ProductFetcher


def run():
   # Bitta super_category id belgilaymiz
    super_id = 1

    # `ProductFetcher` ob'ektini yaratamiz
    fetcher = ProductFetcher(super_id)

    # Jarayonni ishga tushiramiz va natijani olamiz
    result = fetcher.run_process()
    print(result)
    print("dsddsd")