from django.test import TestCase, Client
from django.urls import reverse
from api.models import Category
import json

class CategoryServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

    def test_list_categories(self):
        response = self.client.get(reverse('list_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertEqual(len(data['categories']), 2)
        self.assertEqual(data['categories'][0]['name'], 'Category 1')
        self.assertEqual(data['categories'][1]['name'], 'Category 2')
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['pages'], 1)
        self.assertFalse(data['has_next'])
        self.assertFalse(data['has_previous'])

    def test_get_category_by_id(self):
        response = self.client.get(reverse('get_category_by_id', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Category 1")

    def test_create_category(self):
        response = self.client.post(
            reverse('create_category'),
            data=json.dumps({'name': 'Books'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Books')
        def test_update_category(self):
            update_data = json.dumps({'name': 'Updated Category'})
            response = self.client.put(
                reverse('update_category', args=[self.category1.id]),
                data=update_data,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['name'], 'Updated Category')

            response = self.client.put(
                reverse('update_category', args=[999]),
                data=update_data,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()['error'], 'Category not found.')

            response = self.client.get(reverse('update_category', args=[self.category1.id]))
            self.assertEqual(response.status_code, 405)
            self.assertEqual(response.json()['error'], 'Invalid method.')

        def test_delete_category(self):
            response = self.client.delete(reverse('delete_category', args=[self.category1.id]))
            self.assertEqual(response.status_code, 204)

            response = self.client.delete(reverse('delete_category', args=[999]))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()['error'], 'Category not found.')

            response = self.client.get(reverse('delete_category', args=[self.category1.id]))
            self.assertEqual(response.status_code, 405)
            self.assertEqual(response.json()['error'], 'Invalid method.')