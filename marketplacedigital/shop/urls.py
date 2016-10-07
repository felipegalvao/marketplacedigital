from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'categorias/(?P<category_slug>[\w|-]+)/$', views.show_category, name='show_category'),
    url(r'produtos/criar/$', views.create_product, name='create_product'),
    url(r'produtos/(?P<product_slug>[\w|-]+)/admin/$', views.my_product_admin, name='my_product_admin'),
    url(r'produtos/(?P<product_slug>[\w|-]+)/$', views.show_product, name='show_product'),
]
