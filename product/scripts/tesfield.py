


from product.catelog import ProductFetcher


def run():
    super_id = 1

    # `ProductFetcher` ob'ektini yaratamiz
    fetcher = ProductFetcher(super_id)

    # Jarayonni ishga tushiramiz
    fetcher.run_process()

    # Natijalarni olamiz
    result = fetcher.get_result()
    print(result)
    print("dsddsd")