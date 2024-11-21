import pytest
from api.models import User, Client, Message, Order, OrderItem, Product, Category
from api.serializers.serializers import (
    UserSerializer, ClientSerializer, MessageSerializer,
    OrderSerializer, OrderItemSerializer, ProductSerializer,
)

# Fixtures for common objects
@pytest.fixture
def client():
    return Client.objects.create(
        name='Test Client',
        email='client@example.com',
        phone_number='1234567890',
        city='Test City',
        address='123 Test Street',
    )

@pytest.fixture
def category():
    return Category.objects.create(name='Test Category')

@pytest.fixture
def product(category):
    return Product.objects.create(
        name='Test Product',
        description='A test product',
        price=50.0,
        category=category,
    )

@pytest.fixture
def order(client):
    return Order.objects.create(
        status=Order.Status.IN_PROCESS,  # Use a valid status value from the Status choices
        client=client,
        amount=100.0,  # Ensure amount is a valid value
    )

# Use of parametrize for testing different user data
@pytest.mark.parametrize("user_data", [
    {'name': 'Admin User', 'email': 'admin@example.com', 'password': 'securepassword', 'role': 'admin'},
    {'name': 'Regular User', 'email': 'user@example.com', 'password': 'securepassword', 'role': 'user'},
])
@pytest.mark.django_db
def test_user_serializer(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    for key, value in user_data.items():
        assert getattr(user, key) == value

@pytest.mark.django_db
def test_client_serializer():
    client_data = {
        'name': 'Test Client',
        'email': 'client@example.com',
        'phone_number': '1234567890',
        'city': 'Test City',
        'address': '123 Test Street',  # Ensure the 'address' field is included
    }
    serializer = ClientSerializer(data=client_data)
    assert serializer.is_valid(), serializer.errors
    client = serializer.save()
    for key, value in client_data.items():
        assert getattr(client, key) == value

@pytest.mark.django_db
def test_message_serializer(client):
    message_data = {
        'content': 'Test message',
        'client': client.id,  # Correct relationship to the client
        'name': 'Test Message',  # Required 'name' field
        'description': 'Description of the test message',  # Required 'description'
        'text': 'This is the full message text.'  # Required 'text'
    }
    serializer = MessageSerializer(data=message_data)
    assert serializer.is_valid(), serializer.errors
    message = serializer.save()
    assert message.content == 'Test message'
    assert message.client == client
    assert message.name == 'Test Message'
    assert message.description == 'Description of the test message'
    assert message.text == 'This is the full message text.'

@pytest.mark.django_db
def test_order_item_serializer(order, product):
    order_item_data = {
        'quantity': 1,
        'price': 50.0,
        'order': order.id,
        'product': product.id,
    }
    serializer = OrderItemSerializer(data=order_item_data)
    assert serializer.is_valid(), serializer.errors
    order_item = serializer.save()
    assert order_item.quantity == 1
    assert order_item.price == 50.0
    assert order_item.order == order
    assert order_item.product == product

@pytest.mark.django_db
def test_order_serializer(client):
    order_data = {
        'status': Order.Status.IN_PROCESS,  # Ensure valid status choice
        'client': client.id,  # Correct relationship
        'amount': 100.0,  # Valid amount field
        'payment_method': Order.PaymentMethod.CASH_ON_DELIVERY,  # Add payment method if needed
    }
    serializer = OrderSerializer(data=order_data)
    
    # Check if the order serializer is valid
    assert serializer.is_valid(), serializer.errors
    order = serializer.save()
    assert order.status == Order.Status.IN_PROCESS
    assert order.client == client
    assert order.amount == 100.0  # Ensure 'amount' is correctly set
    assert order.payment_method == Order.PaymentMethod.CASH_ON_DELIVERY  # Ensure payment method is correctly set
