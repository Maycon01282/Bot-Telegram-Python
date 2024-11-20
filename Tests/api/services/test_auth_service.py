from django.test import TestCase
from api.models.user_model import User  # Importar o modelo User correto
from django.contrib.auth import authenticate

class AuthenticateUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', name='Test User', password='testpassword')

    def test_authenticate_user_success(self):
        user = authenticate(username='testuser@example.com', password='testpassword')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    def test_authenticate_user_failure(self):
        user = authenticate(username='testuser@example.com', password='wrongpassword')
        self.assertIsNone(user)