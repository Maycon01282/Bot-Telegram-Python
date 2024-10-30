from django.test import TestCase
from api.models.client_model import Client
from api.services.client_service import list_clients, get_client_by_id, create_client
import json

class ClientServiceTestCase(TestCase):
    def setUp(self):
        self.client1 = Client.objects.create(name='John Doe', phone_number='123456789', city='New York', address='123 Main St', is_active=True)
        self.client2 = Client.objects.create(name='Jane Doe', phone_number='987654321', city='Los Angeles', address='456 Elm St', is_active=True)

    def test_list_clients(self):
        clients = list_clients()
        self.assertEqual(len(clients), 2)
        self.assertEqual(clients[0]['name'], 'John Doe')
        self.assertEqual(clients[1]['name'], 'Jane Doe')

    def test_get_client_by_id(self):
        client = get_client_by_id(self.client1.id)
        self.assertIsNotNone(client)
        self.assertEqual(client['name'], 'John Doe')

        client = get_client_by_id(999)
        self.assertIsNone(client)

    def test_create_client(self):
        data = {
            "name": "New Client",
            "phone_number": "123123123",
            "city": "Chicago",
            "address": "789 Oak St",
            "is_active": True
        }
        client = create_client(data)
        self.assertIsNotNone(client)
        self.assertEqual(client['name'], 'New Client')
        self.assertEqual(client['phone_number'], '123123123')
        self.assertEqual(client['city'], 'Chicago')
        self.assertEqual(client['address'], '789 Oak St')
        self.assertTrue(client['is_active'])