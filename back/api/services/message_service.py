from django.db import models
from ..models import Message

def create_message(name: str, description: str, text: str) -> Message:
    message = Message(name=name, description=description, text=text)
    message.save()
    return message

def get_message_by_id(message_id: int) -> Message:
    return Message.objects.get(id=message_id)

def update_message(message_id: int, name: str = None, description: str = None, text: str = None) -> Message:
    message = Message.objects.get(id=message_id)
    if name:
        message.name = name
    if description:
        message.description = description
    if text:
        message.text = text
    message.save()
    return message

def delete_message(message_id: int) -> None:
    message = Message.objects.get(id=message_id)
    message.delete()
