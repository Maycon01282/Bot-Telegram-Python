# test_client_service.py

from django.test import TestCase
from api.models.client_model import Client
from api.services.client_service import list_clients, get_client_by_id, create_client, update_client, delete_client

class ClientServiceTestCase(TestCase):
    def setUp(self):
        self.client1 = Client.objects.create(
            name="John Doe",
            phone_number="1234567890",
            city="New York",
            address="123 Main St",
            is_active=True
        )
        self.client2 = Client.objects.create(
            name="Jane Smith",
            phone_number="0987654321",
            city="Los Angeles",
            address="456 Elm St",
            is_active=False
        )

    def test_list_clients(self):
        clients = list_clients()
        self.assertEqual(len(clients), 2)
        self.assertEqual(clients[0]['name'], "John Doe")
        self.assertEqual(clients[1]['name'], "Jane Smith")

    def test_get_client_by_id(self):
        client = get_client_by_id(self.client1.id)
        self.assertIsNotNone(client)
        self.assertEqual(client['name'], "John Doe")

        client = get_client_by_id(999)
        self.assertIsNone(client)

    def test_create_client(self):
        data = {
            "name": "Alice Johnson",
            "phone_number": "1112223333",
            "city": "Chicago",
            "address": "789 Oak St",
            "is_active": True
        }
        client = create_client(data)
        self.assertIsNotNone(client)
        self.assertEqual(client['name'], "Alice Johnson")

    def test_update_client(self):
        data = {
            "name": "John Updated",
            "phone_number": "1234567890",
            "city": "New York",
            "address": "123 Main St",
            "is_active": True
        }
        client = update_client(self.client1.id, data)
        self.assertIsNotNone(client)
        self.assertEqual(client['name'], "John Updated")

        client = update_client(999, data)
        self.assertIsNone(client)

    def test_delete_client(self):
        result = delete_client(self.client1.id)
        self.assertTrue(result)
        self.assertEqual(Client.objects.count(), 1)

        result = delete_client(999)
        self.assertFalse(result)