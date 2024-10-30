from django.test import TestCase
from api.models.user_model import User
from api.services.user_service import UserService

class UserServiceTestCase(TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user1 = User.objects.create_user(email="user1@example.com", name="User1", password="password1")
        self.user2 = User.objects.create_user(email="user2@example.com", name="User2", password="password2")

    def test_create_user(self):
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "newpassword"
        }
        result = self.user_service.create_user(data)
        self.assertIsNotNone(result)
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["name"], data["name"])

    def test_update_user_existing(self):
        data = {
            "email": "updateduser1@example.com",
            "name": "Updated User1",
            "password": "updatedpassword1"
        }
        result = self.user_service.update_user(self.user1.id, data)
        self.assertIsNotNone(result)
        self.assertEqual(result["email"], data["email"])
        self.assertEqual(result["name"], data["name"])

    def test_update_user_non_existing(self):
        data = {
            "email": "nonexistinguser@example.com",
            "name": "Non Existing User",
            "password": "nonexistingpassword"
        }
        with self.assertRaises(User.DoesNotExist):
            self.user_service.update_user(999, data)