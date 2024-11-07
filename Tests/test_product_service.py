from django.test import TestCase
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.models import Product
from api.services.product_service import list_products

class ProductServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test products
        for i in range(15):
            Product.objects.create(
                category=f"Category {i}",
                photo_url=f"http://example.com/photo{i}.jpg",
                name=f"Product {i}",
                description=f"Description {i}",
                price=10.0 + i
            )

    def test_list_products_valid_pagination(self):
        response = list_products(page=1, page_size=5)
        self.assertEqual(len(response["products"]), 5)
        self.assertEqual(response["total_pages"], 3)
        self.assertEqual(response["current_page"], 1)
        self.assertTrue(response["has_next"])
        self.assertFalse(response["has_previous"])

    def test_list_products_invalid_page_number(self):
        response = list_products(page="invalid", page_size=5)
        self.assertEqual(response["current_page"], 1)

    def test_list_products_exceeding_page_number(self):
        response = list_products(page=10, page_size=5)
        self.assertEqual(response["current_page"], 3)