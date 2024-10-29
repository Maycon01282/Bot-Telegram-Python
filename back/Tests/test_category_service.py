import json
from django.test import TestCase, Client
from django.urls import reverse
from api.models.category_model import Category

class CategoryServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Home Appliances")

    def test_list_categories(self):
        response = self.client.get(reverse('list_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], "Electronics")
        self.assertEqual(response.json()[1]['name'], "Home Appliances")

    def test_get_category_by_id(self):
        response = self.client.get(reverse('get_category_by_id', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Electronics")

    def test_create_category(self):
        response = self.client.post(
            reverse('create_category'),
            data=json.dumps({'name': 'Books'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Books')