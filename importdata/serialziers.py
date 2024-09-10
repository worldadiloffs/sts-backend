from .models import ImportProduct
from rest_framework import serializers 

class ImportProdcutSerialzeirs(serializers.ModelSerializer):
    class Meta:
        model = ImportProduct
        fields = "__all__"
