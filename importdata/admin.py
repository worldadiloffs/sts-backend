from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ImportProduct , PriceUpdate # Replace with your actual model
from import_export.formats.base_formats import XLS, XLSX, JSON


# Define a resource class
class MyModelResource(resources.ModelResource):
    class Meta:
        model = ImportProduct

# Integrate with admin
@admin.register(ImportProduct)
class MyModelAdmin(ImportExportModelAdmin):
    resource_class = MyModelResource
    formats = [XLSX, JSON] 



class MyModelsPriceUpdateResource(resources.ModelResource):
    class Meta:
        model = PriceUpdate

@admin.register(PriceUpdate)
class ProductPriceUpdateAdmin(ImportExportModelAdmin):
    resource_class = MyModelsPriceUpdateResource
    formats = [XLSX, JSON] 
    