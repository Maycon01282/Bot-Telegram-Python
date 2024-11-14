import unittest
from unittest.mock import patch, MagicMock
from api.services.user_service import UserService
from api.models.user_model import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()

    @patch('api.models.user_model.User.objects.create_user')
    def test_create_user(self, mock_create_user):
        mock_user = MagicMock(id=1, name='Test User', email='test@example.com')
        mock_create_user.return_value = mock_user

        data = {'email': 'test@example.com', 'name': 'Test User', 'password': 'password123'}
        result = self.user_service.create_user(data)

        self.assertEqual(result, {"id": mock_user.id, "name": mock_user.name, "email": mock_user.email})
        mock_create_user.assert_called_once_with(email=data['email'], name=data['name'], password=data['password'])

    @patch('api.models.user_model.User.objects.get')
    def test_update_user(self, mock_get):
        mock_user = MagicMock(id=1, name='Test User', email='test@example.com')
        mock_get.return_value = mock_user

        data = {'name': 'Updated User', 'email': 'updated@example.com', 'password': 'newpassword123'}
        result = self.user_service.update_user(1, data)

        self.assertEqual(result, {"id": mock_user.id, "name": 'Updated User', "email": 'updated@example.com'})
        mock_user.set_password.assert_called_once_with('newpassword123')
        mock_user.save.assert_called_once()

    @patch('api.models.user_model.User.objects.get')
    def test_get_user_by_id(self, mock_get):
        mock_user = MagicMock(id=1, name='Test User', email='test@example.com')
        mock_get.return_value = mock_user

        result = self.user_service.get_user_by_id(1)

        self.assertEqual(result, {"id": mock_user.id, "name": mock_user.name, "email": mock_user.email})
        mock_get.assert_called_once_with(id=1)

    @patch('api.models.user_model.User.objects.get')
    def test_get_user_by_id_not_found(self, mock_get):
        mock_get.side_effect = User.DoesNotExist

        result = self.user_service.get_user_by_id(1)

        self.assertIsNone(result)
        mock_get.assert_called_once_with(id=1)

    @patch('api.models.user_model.User.objects.all')
    def test_list_users(self, mock_all):
        mock_user1 = MagicMock(id=1, name='User One', email='userone@example.com')
        mock_user2 = MagicMock(id=2, name='User Two', email='usertwo@example.com')
        mock_all.return_value = [mock_user1, mock_user2]

        result = self.user_service.list_users(page=1, page_size=1)

        self.assertEqual(result['users'], [{"id": mock_user1.id, "name": mock_user1.name, "email": mock_user1.email}])
        self.assertEqual(result['total_pages'], 2)
        self.assertEqual(result['current_page'], 1)
        self.assertTrue(result['has_next'])
        self.assertFalse(result['has_previous'])

if __name__ == '__main__':
    unittest.main()