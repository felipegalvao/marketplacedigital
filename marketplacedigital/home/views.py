from django.shortcuts import render
from shop.models import Category, Product
import marketplacedigital.settings.base

def home(request):
    print(marketplacedigital.settings.base.BASE_DIR)
    categories = Category.objects.all()
    featured_products = Product.objects.filter(featured=True)
    return render(request, 'home/home.html', { 'categories': categories, 'featured_products': featured_products })
