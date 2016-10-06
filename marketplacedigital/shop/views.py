from django.shortcuts import render
from .models import Category, Product

def show_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    category_products = Product.objects.filter(category=category)
    print(category_products)

    return render(request, 'shop/show_category.html', { 'category_products' : category_products,
                                                        'category': category })

def show_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, 'shop/show_product.html', { 'product': product })
