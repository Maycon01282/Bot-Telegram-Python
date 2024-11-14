from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models.category_model import Category
from api.serializers.serializers import CategorySerializer
from django.contrib.auth.models import User

class CategoryViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')

    def test_list_categories(self):
        url = reverse('list_categories')
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['categories'], serializer.data)

    def test_get_category_by_id(self):
        url = reverse('get_category_by_id', args=[self.category.id])
        response = self.client.get(url)
        serializer = CategorySerializer(self.category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_category(self):
        url = reverse('create_category')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=response.data['id']).name, 'New Category')

    def test_update_category(self):
        url = reverse('update_category', args=[self.category.id])
        data = {'name': 'Updated Category'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect status
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        url = reverse('delete_category', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_list_products_by_category_view(self):
        url = reverse('list_products_by_category_view', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], self.category.name)
        self.assertEqual(response.data['products'], [])