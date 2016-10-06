from django.contrib import admin
from .models import Category, Product, ProductFile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductFile)
