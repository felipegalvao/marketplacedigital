from django.shortcuts import render
from shop.models import Category
import marketplacedigital.settings.base

def home(request):
    print(marketplacedigital.settings.base.BASE_DIR)
    categories = Category.objects.all()
    return render(request, 'home/home.html', { 'categories': categories })
