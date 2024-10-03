from django.db import models

# Create your models here.


class ImportProduct(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    articul = models.IntegerField(blank=True, null=True)
    material_nomer = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.pk} - {self.articul}"




class PriceUpdate(models.Model):
    price = models.FloatField(blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    articul = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.articul}"
