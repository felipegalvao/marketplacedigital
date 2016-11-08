from django.test import TestCase

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .views import register

# class UsersViewsTest(TestCase):    
    # def test_register_page_can_save_POST_request(self):
        # request = HttpRequest()
        # request.user = None
        # request.method = 'POST'
        # request.POST['username'] = 'test_user'
        # request.POST['first_name'] = 'Test'
        # request.POST['last_name'] = 'User'
        # request.POST['email'] = 'linkplace_testuser@gmail.com'
        # request.POST['password1'] = 'absecret12'
        # request.POST['password2'] = 'absecret12'

        # response = register(request)

        # self.assertEqual(User.objects.count(), 1)

        # new_user = User.objects.first()
        # self.assertEqual(new_user.email, 'linkplace_testuser@gmail.com')