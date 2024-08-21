from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    # Agar kerak bo'lsa, formaga qo'shimcha validatsiya yoki logika qo'shing
    def clean_main_category(self):
        title = self.cleaned_data.get('main_category')
        if 'banned' in title.lower():
            raise forms.ValidationError("This title is not allowed!")
        return title