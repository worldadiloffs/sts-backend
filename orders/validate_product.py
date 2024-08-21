from product.models import Product


class ProductValidate:
    def __init__(self, product_id, count, price) -> None:
        self.product_id = product_id
        self.count = count
        self.price = price
        self.validate_product_count()
        self.validate_product_price()

    @staticmethod
    def validate_product_count(product_id, count):
        product = Product.objects.filter(id=product_id).first()
        if product and product.counts >= count:
            return True
        return False
    
    @staticmethod
    def validate_product_price(self):
        product = Product.objects.filter(id=self.product_id).first()
        if product and product.price == self.price:
            return True
        return False

