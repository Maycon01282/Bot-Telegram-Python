import os
import pytest
from rest_framework.exceptions import ValidationError
from api.models.user_model import User
from api.models.category_model import Category
from api.models.client_model import Client
from api.models.message_model import Message
from api.models.order_item_model import OrderItem
from api.models.order_model import Order
from api.models.product_model import Product

from api.serializers.serializers import (
    UserSerializer, CategorySerializer, ClientSerializer, 
    MessageSerializer, OrderItemSerializer, OrderSerializer, 
    ProductSerializer
)

os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'

@pytest.mark.django_db
def test_user_serializer():
    user_data = {'username': 'testuser', 'email': 'test@example.com'}
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()
    user = serializer.save()

@pytest.mark.django_db
def test_category_serializer():
    category_data = {'name': 'Electronics'}
    serializer = CategorySerializer(data=category_data)
    assert serializer.is_valid()
    category = serializer.save()
    assert category.name == 'Electronics'

@pytest.mark.django_db
def test_client_serializer():
    client_data = {'name': 'John Doe', 'email': 'john@example.com'}
    serializer = ClientSerializer(data=client_data)
    assert serializer.is_valid()
    client = serializer.save()
    assert client.name == 'John Doe'
    assert client.email == 'john@example.com'

@pytest.mark.django_db
def test_message_serializer():
    message_data = {'content': 'Hello, World!'}
    serializer = MessageSerializer(data=message_data)
    assert serializer.is_valid()
    message = serializer.save()
    assert message.content == 'Hello, World!'

@pytest.mark.django_db
def test_order_item_serializer():
    order_item_data = {'product': 1, 'quantity': 2}
    serializer = OrderItemSerializer(data=order_item_data)
    assert serializer.is_valid()
    order_item = serializer.save()
    assert order_item.product.id == 1
    assert order_item.quantity == 2

@pytest.mark.django_db
def test_order_serializer():
    order_data = {'client': 1, 'total': 100.0}
    serializer = OrderSerializer(data=order_data)
    assert serializer.is_valid()
    order = serializer.save()
    assert order.client.id == 1
    assert order.total == 100.0

@pytest.mark.django_db
def test_product_serializer():
    category = Category.objects.create(name='Electronics')
    product_data = {
        'name': 'Laptop', 
        'description': 'A powerful laptop', 
        'price': 1500.0, 
        'photo': None, 
        'category': category.id
    }
    serializer = ProductSerializer(data=product_data)
    assert serializer.is_valid()
    product = serializer.save()
    assert product.name == 'Laptop'
    assert product.description == 'A powerful laptop'
    assert product.price == 1500.0
    assert product.category.id == category.id

@pytest.mark.django_db
def test_product_serializer_invalid_price():
    category = Category.objects.create(name='Electronics')
    product_data = {
        'name': 'Laptop', 
        'description': 'A powerful laptop', 
        'price': -1500.0, 
        'photo': None, 
        'category': category.id
    }
    serializer = ProductSerializer(data=product_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db

@pytest.mark.django_db
def test_user_serializer_missing_username():
    user_data = {'email': 'test@example.com'}
    serializer = UserSerializer(data=user_data)
    assert not serializer.is_valid()
    assert 'username' in serializer.errors

@pytest.mark.django_db
def test_category_serializer_empty_name():
    category_data = {'name': ''}
    serializer = CategorySerializer(data=category_data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors

@pytest.mark.django_db
def test_client_serializer_invalid_email():
    client_data = {'name': 'John Doe', 'email': 'invalid-email'}
    serializer = ClientSerializer(data=client_data)
    assert not serializer.is_valid()
    assert 'email' in serializer.errors

@pytest.mark.django_db
def test_message_serializer_empty_content():
    message_data = {'content': ''}
    serializer = MessageSerializer(data=message_data)
    assert not serializer.is_valid()
    assert 'content' in serializer.errors

@pytest.mark.django_db
def test_order_item_serializer_missing_product():
    order_item_data = {'quantity': 2}
    serializer = OrderItemSerializer(data=order_item_data)
    assert not serializer.is_valid()
    assert 'product' in serializer.errors

@pytest.mark.django_db
def test_order_serializer_missing_client():
    order_data = {'total': 100.0}
    serializer = OrderSerializer(data=order_data)
    assert not serializer.is_valid()
    assert 'client' in serializer.errors

@pytest.mark.django_db
def test_product_serializer_missing_name():
    category = Category.objects.create(name='Electronics')
    product_data = {
        'description': 'A powerful laptop', 
        'price': 1500.0, 
        'photo': None, 
        'category': category.id
    }
    serializer = ProductSerializer(data=product_data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors
def test_category_serializer():
    category_data = {'name': 'Electronics'}
    serializer = CategorySerializer(data=category_data)
    assert serializer.is_valid()
    category = serializer.save()
    assert category.name == 'Electronics'

@pytest.mark.django_db
def test_client_serializer():
    client_data = {'name': 'John Doe', 'email': 'john@example.com'}
    serializer = ClientSerializer(data=client_data)
    assert serializer.is_valid()
    client = serializer.save()
    assert client.name == 'John Doe'
    assert client.email == 'john@example.com'

@pytest.mark.django_db
def test_message_serializer():
    message_data = {'content': 'Hello, World!'}
    serializer = MessageSerializer(data=message_data)
    assert serializer.is_valid()
    message = serializer.save()
    assert message.content == 'Hello, World!'

@pytest.mark.django_db
def test_order_item_serializer():
    order_item_data = {'product': 1, 'quantity': 2}
    serializer = OrderItemSerializer(data=order_item_data)
    assert serializer.is_valid()
    order_item = serializer.save()
    assert order_item.product.id == 1
    assert order_item.quantity == 2

@pytest.mark.django_db
def test_order_serializer():
    order_data = {'client': 1, 'total': 100.0}
    serializer = OrderSerializer(data=order_data)
    assert serializer.is_valid()
    order = serializer.save()
    assert order.client.id == 1
    assert order.total == 100.0

@pytest.mark.django_db
def test_product_serializer():
    category = Category.objects.create(name='Electronics')
    product_data = {
        'name': 'Laptop', 
        'description': 'A powerful laptop', 
        'price': 1500.0, 
        'photo': None, 
        'category': category.id
    }
    serializer = ProductSerializer(data=product_data)
    assert serializer.is_valid()
    product = serializer.save()
    assert product.name == 'Laptop'
    assert product.description == 'A powerful laptop'
    assert product.price == 1500.0
    assert product.category.id == category.id

@pytest.mark.django_db
def test_product_serializer_invalid_price():
    category = Category.objects.create(name='Electronics')
    product_data = {
        'name': 'Laptop', 
        'description': 'A powerful laptop', 
        'price': -1500.0, 
        'photo': None, 
        'category': category.id
    }
    serializer = ProductSerializer(data=product_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)