from django.db import models
from autoslug import AutoSlugField

class Categoria(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='name')
    photo = models.ImageField(upload_to='img/categorias/')

    def __str__(self):
        return self.name
