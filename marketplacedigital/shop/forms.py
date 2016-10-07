from django.forms import ModelForm
from .models import Product, ProductFile

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'pay_what_you_want',
                  'category', 'photo']

class ProductFileForm(ModelForm):
    class Meta:
        model = ProductFile
        fields = ['name', 'sample_file', 'uploaded_file']
