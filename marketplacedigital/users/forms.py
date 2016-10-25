#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.forms import AuthenticationForm

from .models import User

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=30, min_length=3, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=100,error_messages={'invalid': ("Email inválido.")}, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=50,min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=50,min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control'}))

    #Override clean method to check password match
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        # Check if passwords match
        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList([u"As senhas não batem."])

        # Check if username already exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            self._errors['username'] = ErrorList([u"Nome de usuário já existe, favor escolher outro."])

        # Check if provided email is already registered
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            self._errors['email'] = ErrorList([u"Este email já está cadastrado."])

        return self.cleaned_data

    #Sending activation email ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #The email is written in a text file (it contains templatetags which are populated by the method below)
    def sendEmail(self, datas):
        link="http://localhost:8000/usuario/ativar/"+datas['activation_key'] # Edit This!
        c=Context({'activation_link':link,'username':datas['username']})
        f = open(MEDIA_ROOT+datas['email_path'], 'r')
        t = Template(f.read())
        f.close()
        message=t.render(c)
        #print unicode(message).encode('utf8')
        send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
