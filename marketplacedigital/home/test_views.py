from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import home

# Create your tests here.
class HomeViewsTest(TestCase):

	def test_root_url_resolves_to_home_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home)

	def test_home_page_returns_proper_html(self):
		request = HttpRequest()
		response = home(request)		
		expected_html = render_to_string('home/home.html')
		self.assertEqual(response.content.decode(), expected_html)