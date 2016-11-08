from selenium import webdriver
import unittest

class NewUserTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_see_categories_and_featured_products(self):
		# User visits the website's homepage
		self.browser.get('http://localhost:8000')

		# User notices the browser title 
		self.assertIn('Linkplace', self.browser.title)

		# User sees a register button, categories and featured products
		self.fail('TO-DO: Finish writing test')



if __name__ == '__main__':  
    unittest.main(warnings='ignore')  