from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views, forms


urlpatterns = [
    url(r'cadastro/$', views.register, name='register'),
    url(r'login/$', views.user_login, name='user_login'),
    url(r'logout/$', views.user_logout, name='user_logout'),
    url(r'minha_conta/meus_dados/$', views.my_user_info, name='my_user_info'),
    url(r'minha_conta/$', views.my_account, name='my_account'),
    url(r'minhas_compras/$', views.my_purchases, name='my_purchases'),
    url(r'minhas_vendas/$', views.my_sales, name='my_sales'),
    url(r'minhas_compras/(?P<purchase_id>[0-9]+)/$', views.show_purchase, name='show_purchase'),
    url(r'minhas_compras/acessar_arquivo/(?P<file_id>[0-9]+)/$', views.send_file, name='send_file'),
    url(r'minhas_compras/notificacao_pagseguro/$', views.notificacao_pagseguro, name='notificacao_pagseguro'),
    url(r'ativar/(?P<activation_key>\w+)$', views.activate, name='activate'),
    url(r'resetar_senha/$', auth_views.password_reset, {'template_name': 'users/password_reset.html'}, name='password_reset'),
    url(r'resetar_senha/concluido/$', auth_views.password_reset_done, {'template_name': 'users/password_reset_done.html'}, name='password_reset_done'),
    url(r'resetar_senha/confirmar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'users/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'resetar_senha/completar/$', auth_views.password_reset_complete, {'template_name': 'users/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'reenviar_email_ativacao/$', views.resend_activation_email, name='resend_activation_email')
]
