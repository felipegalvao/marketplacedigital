from django.shortcuts import render
from shop.models import Category

def home(request):
    categories = Category.objects.all()
    return render(request, 'home/home.html', { 'categories': categories })
