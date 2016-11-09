from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Imports for email sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Category, Product, ProductFile, Purchase
from .forms import ProductForm, ProductFileForm
from users.models import Profile
from marketplacedigital.settings.project_utils import calculate_seller_commission
from marketplacedigital.settings import settings_secrets

import requests

def show_category(request, category_slug):
    '''Show all products from a Category'''
    category = Category.objects.get(slug=category_slug)
    category_products = Product.objects.filter(category=category, approved=True)

    return render(request, 'shop/show_category.html', { 'category_products' : category_products,
                                                        'category': category })

def show_product(request, product_slug):
    '''Show product details'''
    product = Product.objects.get(slug=product_slug)
    profile = Profile.objects.get(user=product.user)
    product_files_sample = product.files.filter(sample_file=True, approved=True)
    product_files_not_sample = product.files.filter(sample_file=False, approved=True)
    if not product_files_not_sample:
        messages.info(request, 'Pedimos desculpas, mas os arquivos referentes a este produto ainda não foram aprovados. Favor selecionar outro produto ou retornar posteriormente.')
        return redirect('/')
    product_files = product.files.all()
    return render(request, 'shop/show_product.html', { 'product': product, 'product_files_sample': product_files_sample,
                                                       'product_files_not_sample': product_files_not_sample,
                                                       'product_files': product_files,
                                                       'profile': profile})

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

    purchase_confirmation_email(purchase)
    sale_confirmation_email(purchase)

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

@csrf_exempt
def notificacao_pagseguro(request):
    if request.method == 'POST':
        request.encoding = 'ISO-8859-1'
        notification_code = request.POST['notificationCode']
        notification_type = request.POST['notificationType']

        dados_consulta = {
            "email": settings_secrets.PAGSEGURO_EMAIL,
            "token": settings_secrets.PAGSEGURO_TOKEN_SANDBOX
        }

        request_link = "https://ws.sandbox.pagseguro.uol.com.br/v3/transactions/notifications/" + notification_code

        r = requests.get(request_link, params=dados_consulta)
        r_texto = r.text

        purchase_id = find_between(r_texto, "<reference>","</reference>")
        transaction_status = find_between(r_texto, "<status>","</status>")

        purchase = Purchase.objects.get(pk=int(purchase_id))
        if transaction_status == "3":
            purchase.paid = True
            purchase.save()

            purchase_paid_email(purchase)
            sale_paid_email(purchase)
        return HttpResponse('OK')
    else:
        return redirect('/')

def search_products(request):
    search_string = request.GET.get('q', "")
    if search_string:
        products = Product.objects.filter(Q(name__icontains=search_string) | Q(description__icontains=search_string)).filter(approved=True)
    else:
        products = None
    return render(request, 'shop/search_products.html', { 'products': products })

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def purchase_confirmation_email(purchase):    
    link = 'usuario/minhas_compras/'
    my_purchases_link = settings.BASE_DOMAIN + link

    email_subject = "Linkplace - Sua compra foi realizada"    
    to_email = purchase.user.email

    template_name = 'purchase_confirmation_email'

    context = { 'purchase': purchase, 'my_purchases_link': my_purchases_link }

    send_transaction_email(email_subject, template_name, context, to_email)
    

def sale_confirmation_email(purchase):    
    link = 'usuario/minhas_vendas/'
    my_sales_link = settings.BASE_DOMAIN + link

    email_subject = "Linkplace - Você acaba de realizar uma venda"    
    to_email = purchase.product.user.email

    template_name = 'sale_confirmation_email'    

    context = { 'purchase': purchase, 'my_sales_link': my_sales_link }

    send_transaction_email(email_subject, template_name, context, to_email)

def purchase_paid_email(purchase):    
    link = 'usuario/minhas_compras/'
    my_purchases_link = settings.BASE_DOMAIN + link

    email_subject = "Linkplace - O pagamento para sua compra foi confirmado"
    to_email = purchase.user.email

    template_name = 'purchase_paid_email'

    context = { 'purchase': purchase, 'my_purchases_link': my_purchases_link }

    send_transaction_email(email_subject, template_name, context, to_email)

def sale_paid_email(purchase):
    link = 'usuario/minhas_vendas/'
    my_sales_link = settings.BASE_DOMAIN + link

    email_subject = "Linkplace - O pagamento para sua venda foi confirmado."
    to_email = purchase.product.user.email

    template_name = 'sale_paid_email'

    context = { 'purchase': purchase, 'my_sales_link': my_sales_link }

    send_transaction_email(email_subject, template_name, context, to_email)

def send_transaction_email(email_subject, template_name, context, to_email):
    from_email = "felipect86@gmail.com"    

    text_template = get_template('shop/emails/' + template_name + '.txt')
    html_template = get_template('shop/emails/' + template_name + '.html')

    d = Context(context)

    text_content = text_template.render(d)
    html_content = html_template.render(d)

    msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()