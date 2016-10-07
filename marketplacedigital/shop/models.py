from django.db import models
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='name')
    photo = models.ImageField(upload_to='img/categorias/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='name')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pay_what_you_want = models.BooleanField()
    category = models.ForeignKey(Category)
    photo = models.ImageField(upload_to='img/produtos/')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ProductFile(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='files')
    sample_file = models.BooleanField()
    uploaded_file = models.FileField(upload_to='arquivos/upload_usuario')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return(self.product.name + " - " + self.name)
