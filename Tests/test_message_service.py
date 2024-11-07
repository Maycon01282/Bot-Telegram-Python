from django.test import TestCase
from api.models.message_model import Message
from api.services.message_service import create_message, get_message_by_id, update_message
from api.services.message_service import create_message, get_message_by_id, update_message, delete_message

class MessageServiceTestCase(TestCase):
    def setUp(self):
        self.message = create_message(name='Test Message', description='Test Description', text='Test Text')

class MessageServiceTestCase(TestCase):
    def setUp(self):
        self.message = create_message(name='Test Message', description='Test Description', text='Test Text')

    def test_create_message(self):
        message = create_message(name='New Message', description='New Description', text='New Text')
        self.assertIsInstance(message, Message)
        self.assertEqual(message.name, 'New Message')
        self.assertEqual(message.description, 'New Description')
        self.assertEqual(message.text, 'New Text')

    def test_get_message_by_id(self):
        message = get_message_by_id(self.message.id)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.name, 'Test Message')
        self.assertEqual(message.description, 'Test Description')
        self.assertEqual(message.text, 'Test Text')

    def test_update_message(self):
        updated_message = update_message(self.message.id, name='Updated Message', description='Updated Description', text='Updated Text')
        self.assertIsInstance(updated_message, Message)
        self.assertEqual(updated_message.name, 'Updated Message')
        self.assertEqual(updated_message.description, 'Updated Description')
        self.assertEqual(updated_message.text, 'Updated Text')

        def test_delete_message(self):
            delete_message(self.message.id)
            with self.assertRaises(Message.DoesNotExist):
                get_message_by_id(self.message.id)
                def test_update_message(self):
                    # Test successful update
                    updated_message = update_message(self.message.id, name='Updated Message', description='Updated Description', text='Updated Text')
                    self.assertIsInstance(updated_message, Message)
                    self.assertEqual(updated_message.name, 'Updated Message')
                    self.assertEqual(updated_message.description, 'Updated Description')
                    self.assertEqual(updated_message.text, 'Updated Text')

                    # Test updating a non-existent message
                    with self.assertRaises(Message.DoesNotExist):
                        update_message(999, name='Non-existent Message')

                    # Test updating with partial data
                    updated_message = update_message(self.message.id, name='Partially Updated Message')
                    self.assertEqual(updated_message.name, 'Partially Updated Message')
                    self.assertEqual(updated_message.description, 'Test Description')
                    self.assertEqual(updated_message.text, 'Test Text')

                    updated_message = update_message(self.message.id, description='Partially Updated Description')
                    self.assertEqual(updated_message.name, 'Partially Updated Message')
                    self.assertEqual(updated_message.description, 'Partially Updated Description')
                    self.assertEqual(updated_message.text, 'Test Text')

                    updated_message = update_message(self.message.id, text='Partially Updated Text')
                    self.assertEqual(updated_message.name, 'Partially Updated Message')
                    self.assertEqual(updated_message.description, 'Partially Updated Description')
                    self.assertEqual(updated_message.text, 'Partially Updated Text')