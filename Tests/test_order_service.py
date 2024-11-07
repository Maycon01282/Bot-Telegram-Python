from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from api.models import Order, Client
from api.services.order_service import get_order_by_id, update_order, delete_order, list_orders

class OrderServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test client and orders
        cls.client = Client.objects.create(name="Client 1", email="client1@example.com")
        cls.order = Order.objects.create(client=cls.client, status="Pending", amount=100.0)
        for i in range(15):
            Order.objects.create(client=cls.client, status="Pending", amount=100.0 + i)

    def test_get_order_by_id_success(self):
        order = get_order_by_id(self.order.id)
        self.assertEqual(order.client.name, "Client 1")

    def test_get_order_by_id_non_existent(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_order_by_id(999)

    def test_update_order_success(self):
        updated_order = update_order(self.order.id, client=self.client, status="Completed", amount=200.0)
        self.assertEqual(updated_order.client.name, "Client 1")
        self.assertEqual(updated_order.status, "Completed")
        self.assertEqual(updated_order.amount, 200.0)

    def test_update_order_non_existent(self):
        with self.assertRaises(ObjectDoesNotExist):
            update_order(999, client=self.client, status="Completed", amount=200.0)

    def test_update_order_invalid_status(self):
        with self.assertRaises(ValueError):
            update_order(self.order.id, status="InvalidStatus")

    def test_update_order_partial_data(self):
        updated_order = update_order(self.order.id, client=self.client)
        self.assertEqual(updated_order.client.name, "Client 1")
        self.assertEqual(updated_order.status, "Pending")
        self.assertEqual(updated_order.amount, 100.0)

    def test_delete_order_success(self):
        delete_order(self.order.id)
        with self.assertRaises(ObjectDoesNotExist):
            Order.objects.get(id=self.order.id)

    def test_delete_order_non_existent(self):
        with self.assertRaises(ObjectDoesNotExist):
            delete_order(999)

    def test_list_orders_valid_pagination(self):
        response = list_orders(page=1, page_size=5)
        self.assertEqual(len(response["orders"]), 5)
        self.assertEqual(response["total_pages"], 4)
        self.assertEqual(response["current_page"], 1)
        self.assertTrue(response["has_next"])
        self.assertFalse(response["has_previous"])

    def test_list_orders_invalid_page_number(self):
        response = list_orders(page="invalid", page_size=5)
        self.assertEqual(response["current_page"], 1)

    def test_list_orders_exceeding_page_number(self):
        response = list_orders(page=10, page_size=5)
        self.assertEqual(response["current_page"], 4)