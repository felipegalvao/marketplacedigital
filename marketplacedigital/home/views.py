from django.shortcuts import render
from shop.models import Categoria

def home(request):
    categorias = Categoria.objects.all()
    return render(request, 'home/home.html', { 'categorias': categorias })
