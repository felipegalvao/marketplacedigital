#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.utils import ErrorList
from .models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=3, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=100,error_messages={'invalid': ("Email inválido.")})
    password1 = forms.CharField(max_length=50,min_length=6)
    password2 = forms.CharField(max_length=50,min_length=6)

    #Override clean method to check password match
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList([u"As senhas não batem."])

        user = User.objects.get(username=username)
        if user:
            self._errors['username'] = ErrorList([u"Nome de usuário já existe, favor escolher outro."])

        return self.cleaned_data

    #Sending activation email ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #The email is written in a text file (it contains templatetags which are populated by the method below)
    def sendEmail(self, datas):
        link="http://yourdomain.com/activate/"+datas['activation_key'] # Edit This!
        c=Context({'activation_link':link,'username':datas['username']})
        f = open(MEDIA_ROOT+datas['email_path'], 'r')
        t = Template(f.read())
        f.close()
        message=t.render(c)
        #print unicode(message).encode('utf8')
        send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
