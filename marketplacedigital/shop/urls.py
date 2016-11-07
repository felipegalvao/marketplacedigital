from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'pesquisar/$', views.search_products, name='search_products'),
    url(r'categorias/(?P<category_slug>[\w|-]+)/$', views.show_category, name='show_category'),
    url(r'produtos/criar/$', views.create_product, name='create_product'),
    url(r'produtos/meus_produtos/$', views.my_products, name='my_products'),
    url(r'produtos/(?P<product_slug>[\w|-]+)/admin/$', views.my_product_admin, name='my_product_admin'),
    url(r'produtos/(?P<product_slug>[\w|-]+)/comprar/$', views.product_purchase, name='product_purchase'),
    url(r'produtos/(?P<product_slug>[\w|-]+)/fechar_compra/$', views.purchase_confirmation, name='purchase_confirmation'),
    url(r'produtos/(?P<product_slug>[\w|-]+)/$', views.show_product, name='show_product'),
    url(r'compras/notificacao_pagseguro/$', views.notificacao_pagseguro, name='notificacao_pagseguro'),
]
