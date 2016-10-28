from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Category, Product, ProductFile, Purchase
from .forms import ProductForm, ProductFileForm
from marketplacedigital.settings.project_utils import calculate_seller_commission

import requests

def show_category(request, category_slug):
    '''Show all products from a Category'''
    category = Category.objects.get(slug=category_slug)
    category_products = Product.objects.filter(category=category, approved=True, files__isnull=False)

    return render(request, 'shop/show_category.html', { 'category_products' : category_products,
                                                        'category': category })

def show_product(request, product_slug):
    '''Show product details'''
    product = Product.objects.get(slug=product_slug)
    product_files_sample = product.files.filter(sample_file=True, approved=True)
    product_files_not_sample = product.files.filter(sample_file=False, approved=True)
    if not product_files_not_sample:
        messages.info(request, 'Pedimos desculpas, mas os arquivos referentes a este produto ainda não foram aprovados. Favor selecionar outro produto ou retornar posteriormente.')
        return redirect('/')
    product_files = product.files.all()
    return render(request, 'shop/show_product.html', { 'product': product, 'product_files_sample': product_files_sample,
                                                       'product_files_not_sample': product_files_not_sample,
                                                       'product_files': product_files})

@login_required(login_url='/usuario/login/')
def create_product(request):
    '''Create a new product'''
    categories = Category.objects.all()
    error = ''
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            return HttpResponseRedirect(reverse('my_product_admin', args=(product.slug,)))
        else:
            error = 'Dados inválidos. Favor preencher novamente o formulário.'
            print(error)
            print(product_form.errors)

    product_form = ProductForm()
    return render(request, 'shop/create_product.html', { 'error': error, 'categories': categories, 'product_form': product_form })

@login_required(login_url='/usuario/login/')
def my_product_admin(request, product_slug):
    '''View for the user to manage a product he created'''
    product = Product.objects.get(slug=product_slug)
    if product.user != request.user:
        messages.warning(request, 'Você não tem autorização para acessar esta página.')
        return redirect('/')
    product_files = product.files.all()
    error = ''
    if request.method == 'POST':
        product_file_form = ProductFileForm(request.POST, request.FILES)
        if product_file_form.is_valid():
            product_file = product_file_form.save(commit=False)
            product_file.product = product
            product_file.save()
            return HttpResponseRedirect(reverse('my_product_admin', args=(product.slug,)))
        else:
            error = 'Dados inválidos. Favor preencher novamente o formulário.'
            print(error)
            print(product_file_form.errors)

    product_file_form = ProductFileForm()
    return render(request, 'shop/my_product_admin.html', { 'error': error, 'product': product, 'product_files': product_files })

@login_required(login_url='/usuario/login/')
def my_products(request):
    '''View that returns all of a user products'''
    products = Product.objects.filter(user=request.user)
    return render(request, 'shop/my_products.html', { 'products': products })

@login_required(login_url='/usuario/login/')
def product_purchase(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    purchase = Purchase.objects.filter(user=request.user, product=product)
    if purchase:
        messages.warning(request, 'Você já comprou este produto, não é necessário comprar novamente.')
        return redirect('/')

    if product.user == request.user:
        messages.warning(request, 'Este produto é seu, você não precisa comprá-lo.')
        return redirect('/')

    return render(request, 'shop/product_purchase.html', { 'product': product })

@login_required(login_url='/usuario/login/')
def purchase_confirmation(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    purchase = Purchase(user = request.user,
                        product = product,
                        value = product.price,
                        paid = False,
                        seller_commission=calculate_seller_commission(product.price))
    purchase.save()

    dados_pagamento = {
        "email":"felipect86@gmail.com",
        "token":"A90C580ABDB1475296FCCDED71E91C04",
        "currency":"BRL",
        "reference":str(purchase.id),
        # "senderName": request.user.first_name + ' ' + request.user.last_name,
        "senderEmail": str(request.user.email),
        "itemId1" : "001",
        "itemDescription1" : "Pagamento do produto - " + product.name,
        "itemAmount1" : str(product.price),
        "itemQuantity1" : "1",
    }

    print(dados_pagamento)

    codigo_pagamento = ""
    r = requests.post("https://ws.sandbox.pagseguro.uol.com.br/v2/checkout", data=dados_pagamento)
    r_texto = r.text
    codigo_pagamento = find_between(r_texto, "<code>","</code>")

    print(r_texto)

    return redirect('https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code=' + codigo_pagamento)

    messages.success(request, 'Sua compra foi concluída. Assim que seu pagamento for aprovado, você será notificado e poderá acessar os seus arquivos.')
    return redirect('/')

def search_products(request):
    search_string = request.GET['q']
    products = Product.objects.filter(Q(name__icontains=search_string) | Q(description__icontains=search_string)).filter(approved=True)
    return render(request, 'shop/search_products.html', { 'products': products })

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
