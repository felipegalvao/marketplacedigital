from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'cadastro/$', views.register, name='register'),    
]
