from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from api.models import OrderItem, Order
from api.services.order_item_service import update_order_item, delete_order_item

class OrderItemServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test order and order items
        cls.order = Order.objects.create(client="Client 1", status="Pending", amount=100.0)
        cls.order_item = OrderItem.objects.create(order=cls.order, quantity=10)

    def test_update_order_item_success(self):
        updated_order_item = update_order_item(self.order_item.id, quantity=20)
        self.assertEqual(updated_order_item.quantity, 20)

    def test_update_order_item_non_existent(self):
        with self.assertRaises(ObjectDoesNotExist):
            update_order_item(999, quantity=20)

    def test_update_order_item_no_quantity(self):
        updated_order_item = update_order_item(self.order_item.id)
        self.assertEqual(updated_order_item.quantity, 10)  # Quantity should remain unchanged

    def test_delete_order_item_success(self):
        delete_order_item(self.order_item.id)
        with self.assertRaises(ObjectDoesNotExist):
            OrderItem.objects.get(id=self.order_item.id)

    def test_delete_order_item_non_existent(self):
        with self.assertRaises(ObjectDoesNotExist):
            delete_order_item(999)