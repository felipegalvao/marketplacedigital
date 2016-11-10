from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

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

    def __str__(self):
        return(self.user.username + ' - ' + self.product.name)
