from django.test import TestCase
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.models import User
from api.services.user_service import list_users

class UserServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        for i in range(15):
            User.objects.create(name=f"User {i}", email=f"user{i}@example.com")

    def test_list_users_valid_pagination(self):
        response = list_users(page=1, page_size=5)
        self.assertEqual(len(response["users"]), 5)
        self.assertEqual(response["total_pages"], 3)
        self.assertEqual(response["current_page"], 1)
        self.assertTrue(response["has_next"])
        self.assertFalse(response["has_previous"])

    def test_list_users_invalid_page_number(self):
        response = list_users(page="invalid", page_size=5)
        self.assertEqual(response["current_page"], 1)

    def test_list_users_exceeding_page_number(self):
        response = list_users(page=10, page_size=5)
        self.assertEqual(response["current_page"], 3)