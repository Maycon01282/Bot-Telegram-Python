# test_product_service.py

from django.test import TestCase
from api.models.product_model import Product
from api.models.category_model import Category
from api.services.product_service import list_products, get_product_by_id, create_product, update_product, delete_product

class ProductServiceTestCase(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Home Appliances")

        self.product1 = Product.objects.create(
            category=self.category1,
            photo_url="http://example.com/photo1.jpg",
            name="Smartphone",
            description="A smartphone with many features",
            price=299.99
        )
        self.product2 = Product.objects.create(
            category=self.category2,
            photo_url="http://example.com/photo2.jpg",
            name="Vacuum Cleaner",
            description="A powerful vacuum cleaner",
            price=99.99
        )

    def test_list_products(self):
        products = list_products()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['name'], "Smartphone")
        self.assertEqual(products[1]['name'], "Vacuum Cleaner")

    def test_get_product_by_id(self):
        product = get_product_by_id(self.product1.id)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "Smartphone")

        product = get_product_by_id(999)
        self.assertIsNone(product)

    def test_create_product(self):
        data = {
            "category": self.category1,
            "photo_url": "http://example.com/photo3.jpg",
            "name": "Python Programming",
            "description": "A book about Python programming",
            "price": 39.99
        }
        product = create_product(data)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "Python Programming")

    def test_update_product(self):
        data = {
            "category": self.category1,
            "photo_url": "http://example.com/photo1.jpg",
            "name": "Smartphone Updated",
            "description": "An updated smartphone with many features",
            "price": 299.99
        }
        product = update_product(self.product1.id, data)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "Smartphone Updated")

        product = update_product(999, data)
        self.assertIsNone(product)

    def test_delete_product(self):
        result = delete_product(self.product1.id)
        self.assertTrue(result)
        self.assertEqual(Product.objects.count(), 1)

        result = delete_product(999)
        self.assertFalse(result)