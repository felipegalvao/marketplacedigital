from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Imports for email sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

import requests
from decimal import Decimal

from marketplacedigital.settings.project_utils import find_between
from marketplacedigital.settings import settings_secrets

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='name')
    photo = models.ImageField(upload_to='img/categorias/')

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pay_what_you_want = models.BooleanField()
    category = models.ForeignKey(Category)
    photo = models.ImageField(upload_to='img/produtos/')
    approved = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def minimum_value(self):
        return(int(self.price))

    def maximum_value(self):
        return(int(self.price * 5))

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if instance.sample_file == True:
        return 'user_uploaded/sample/{0}/{1}/{2}'.format(instance.product.user.id, instance.product.id, filename)
    else:
        return 'user_uploaded/protected/{0}/{1}/{2}'.format(instance.product.user.id, instance.product.id, filename)

class ProductFile(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='files')
    sample_file = models.BooleanField()
    uploaded_file = models.FileField(upload_to=user_directory_path)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return(self.product.name + " - " + self.name)

class Purchase(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)
    seller_commission = models.DecimalField(max_digits=6, decimal_places=2)
    payment_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return(self.user.username + ' - ' + self.product.name)

    def request_payment_code_to_pagseguro(self):
        payment_data = {
            "email": settings_secrets.PAGSEGURO_EMAIL,
            "token":settings_secrets.PAGSEGURO_TOKEN_SANDBOX,
            "currency":"BRL",
            "reference":str(self.id),
            # "senderName": request.user.first_name + ' ' + request.user.last_name,
            "senderEmail": str(self.user.email),
            "itemId1" : "001",
            "itemDescription1" : "Pagamento do produto - " + self.product.name,
            "itemAmount1" : "{0:.2f}".format(self.value),
            "itemQuantity1" : "1",
        }

        payment_code = ""
        r = requests.post("https://ws.sandbox.pagseguro.uol.com.br/v2/checkout", data=payment_data)
        r_text = r.text
        payment_code = find_between(r_text, "<code>","</code>") 

        return(payment_code)

    def purchase_confirmation_email(self):
        link = 'usuario/minhas_compras/'
        my_purchases_link = settings.BASE_DOMAIN + link

        email_subject = "Linkplace - Sua compra foi realizada"    
        to_email = self.user.email

        template_name = 'purchase_confirmation_email'

        context = { 'purchase': self, 'my_purchases_link': my_purchases_link }

        self.send_transaction_email(email_subject, template_name, context, to_email)

    def sale_confirmation_email(self):    
        link = 'usuario/minhas_vendas/'
        my_sales_link = settings.BASE_DOMAIN + link

        email_subject = "Linkplace - Você acaba de realizar uma venda"    
        to_email = self.product.user.email

        template_name = 'sale_confirmation_email'    

        context = { 'purchase': self, 'my_sales_link': my_sales_link }

        self.send_transaction_email(email_subject, template_name, context, to_email)

    def purchase_paid_email(self):    
        link = 'usuario/minhas_compras/'
        my_purchases_link = settings.BASE_DOMAIN + link

        email_subject = "Linkplace - O pagamento para sua compra foi confirmado"
        to_email = self.user.email

        template_name = 'purchase_paid_email'

        context = { 'purchase': self, 'my_purchases_link': my_purchases_link }

        self.send_transaction_email(email_subject, template_name, context, to_email)

    def sale_paid_email(self):
        link = 'usuario/minhas_vendas/'
        my_sales_link = settings.BASE_DOMAIN + link

        email_subject = "Linkplace - O pagamento para sua venda foi confirmado."
        to_email = self.product.user.email

        template_name = 'sale_paid_email'

        context = { 'purchase': self, 'my_sales_link': my_sales_link }

        self.send_transaction_email(email_subject, template_name, context, to_email)

    def send_transaction_email(self, email_subject, template_name, context, to_email):
        from_email = "felipect86@gmail.com"    

        text_template = get_template('shop/emails/' + template_name + '.txt')
        html_template = get_template('shop/emails/' + template_name + '.html')

        d = Context(context)

        text_content = text_template.render(d)
        html_content = html_template.render(d)

        msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def calculate_seller_commission(self, sale_value):
        seller_commission = (Decimal(sale_value) * Decimal(0.85)) - Decimal(0.50)
        self.seller_commission = seller_commission
        self.save()
