from django.test import TestCase
from api.models.order_model import Order
from api.models.client_model import Client  # Assuming there is a Client model
from api.services.order_service import get_order_by_id

class OrderServiceTestCase(TestCase):
    def setUp(self):
        self.client1 = Client.objects.create(name="Client1")
        self.client2 = Client.objects.create(name="Client2")
        self.order1 = Order.objects.create(client=self.client1, status="Pending", amount=100.0)
        self.order2 = Order.objects.create(client=self.client2, status="Completed", amount=200.0)

    def test_get_order_by_id_existing(self):
        order = get_order_by_id(self.order1.id)
        self.assertIsNotNone(order)
        self.assertEqual(order.client, self.client1)
        self.assertEqual(order.status, "Pending")
        self.assertEqual(order.amount, 100.0)

    def test_get_order_by_id_non_existing(self):
        with self.assertRaises(Order.DoesNotExist):
            get_order_by_id(999)