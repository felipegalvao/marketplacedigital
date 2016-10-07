from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Category, Product, ProductFile
from .forms import ProductForm, ProductFileForm

def show_category(request, category_slug):
    '''Show all products from a Category'''
    category = Category.objects.get(slug=category_slug)
    category_products = Product.objects.filter(category=category)

    return render(request, 'shop/show_category.html', { 'category_products' : category_products,
                                                        'category': category })

def show_product(request, product_slug):
    '''Show product details'''
    product = Product.objects.get(slug=product_slug)
    product_files = product.files.all()
    return render(request, 'shop/show_product.html', { 'product': product, 'product_files': product_files })

def create_product(request):
    '''Create a new product'''
    categories = Category.objects.all()
    error = ''
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            # product.user = request.user
            product.save()
            return HttpResponseRedirect(reverse('my_product_admin', args=(product.slug,)))
        else:
            error = 'Dados inválidos. Favor preencher novamente o formulário.'
            print(error)
            print(product_form.errors)

    product_form = ProductForm()
    return render(request, 'shop/create_product.html', { 'error': error, 'categories': categories, 'product_form': product_form })

def my_product_admin(request, product_slug):
    '''View for the user to manage a product he created'''
    product = Product.objects.get(slug=product_slug)
    product_files = product.files.all()
    error = ''
    if request.method == 'POST':
        product_file_form = ProductFileForm(request.POST, request.FILES)
        if product_file_form.is_valid():
            product_file = product_file_form.save(commit=False)
            product_file.product = product
            product_file.save()
        else:
            error = 'Dados inválidos. Favor preencher novamente o formulário.'
            print(error)
            print(product_file_form.errors)

    product_file_form = ProductFileForm()
    return render(request, 'shop/my_product_admin.html', { 'error': error, 'product': product, 'product_files': product_files })
