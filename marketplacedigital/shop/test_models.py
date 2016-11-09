from django.test import TestCase
from model_mommy import mommy

from .models import Category, Product, ProductFile, Purchase

class ShopTestMommy(TestCase):

    def test_category_creation_mommy(self):
        new_category = mommy.make(Category)

        self.assertTrue(isinstance(new_category, Category))
        self.assertEqual(new_category.__str__(), new_category.name)

    def test_product_creation_mommy(self):
        new_product = mommy.make(Product)

        self.assertTrue(isinstance(new_product, Product))
        self.assertEqual(new_product.__str__(), new_product.name)

    def test_product_file_creation_mommy(self):
        new_product_file_sample = mommy.make(ProductFile, sample_file=True)
        new_product_file_not_sample = mommy.make(ProductFile, sample_file=False)

        self.assertTrue(isinstance(new_product_file_sample, ProductFile))
        self.assertEqual(new_product_file_sample.__str__(), new_product_file_sample.product.name + " - " + new_product_file_sample.name)

        self.assertIn('user_uploaded/protected', new_product_file_not_sample.uploaded_file.path)
        self.assertIn('user_uploaded/sample', new_product_file_sample.uploaded_file.path)
    

    def test_purchase_creation_mommy(self):
        new_purchase = mommy.make(Purchase)

        self.assertTrue(isinstance(new_purchase, Purchase))
        self.assertEqual(new_purchase.__str__(), new_purchase.user.username + " - " + new_purchase.product.name)
