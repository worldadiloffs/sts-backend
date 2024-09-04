from django.db import models
from account.models import User
from category.models import SuperCategory , MainCategory , SubCategory

# Create your models here.


# class CalculatorProduct(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
#     token = models.CharField(max_length=255, blank=True)
#     order_id = models.IntegerField(blank=True, null=True)
#     product = models.JSONField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True)





# class CalculatorAi(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
#     category = models.ForeignKey(SuperCategory, on_delete=models.CASCADE, blank=True)
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True)
#     product = models.JSONField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, blank=True)