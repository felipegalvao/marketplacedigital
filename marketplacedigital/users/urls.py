from django.conf.urls import url
from . import views, forms


urlpatterns = [
    url(r'cadastro/$', views.register, name='register'),
    url(r'login/$', views.user_login, name='user_login'),
    url(r'logout/$', views.user_logout, name='user_logout'),
    url(r'minhas_compras/$', views.my_purchases, name='my_purchases'),
    url(r'minhas_compras/(?P<purchase_id>[0-9]+)/$', views.show_purchase, name='show_purchase'),
    url(r'ativar/(?P<activation_key>\w+)$', views.activate, name='activate'),
]
