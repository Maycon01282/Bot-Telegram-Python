from django.test import TestCase
from api.models.order_item_model import OrderItem
from api.models.order_model import Order
from api.models.product_model import Product
from api.models.client_model import Client  # Import the Client model
from api.services.order_item_service import create_order_item, get_order_item_by_id, update_order_item, delete_order_item, list_order_items_by_order

class OrderItemServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='Test Client')  # Create a test client
        self.order = Order.objects.create(client=self.client, amount=1000)
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.order_item = create_order_item(order_id=self.order.id, product_id=self.product.id, quantity=5)

    def test_create_order_item(self):
        order_item = create_order_item(order_id=self.order.id, product_id=self.product.id, quantity=3)
        self.assertIsInstance(order_item, OrderItem)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 3)

    def test_get_order_item_by_id(self):
        order_item = get_order_item_by_id(self.order_item.id)
        self.assertIsInstance(order_item, OrderItem)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 5)

    def test_update_order_item(self):
        updated_order_item = update_order_item(self.order_item.id, quantity=10)
        self.assertIsInstance(updated_order_item, OrderItem)
        self.assertEqual(updated_order_item.quantity, 10)

    def test_delete_order_item(self):
        delete_order_item(self.order_item.id)
        with self.assertRaises(OrderItem.DoesNotExist):
            OrderItem.objects.get(id=self.order_item.id)

    def test_list_order_items_by_order(self):
        order_items = list_order_items_by_order(self.order.id)
        self.assertIsInstance(order_items, list)
        self.assertEqual(len(order_items), 1)
        self.assertEqual(order_items[0], self.order_item)