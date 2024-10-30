from api.models.client_model import Client
from django.core.exceptions import ObjectDoesNotExist

def list_clients():
    clients = Client.objects.all()
    return [{"id": client.id, "name": client.name, "phone_number": client.phone_number, "city": client.city, "address": client.address, "is_active": client.is_active} for client in clients]

def get_client_by_id(client_id):
    try:
        client = Client.objects.get(id=client_id)
        return {"id": client.id, "name": client.name, "phone_number": client.phone_number, "city": client.city, "address": client.address, "is_active": client.is_active}
    except ObjectDoesNotExist:
        return None

def create_client(data):
    client = Client.objects.create(
        name=data['name'],
        phone_number=data['phone_number'],
        city=data['city'],
        address=data['address'],
        is_active=data.get('is_active', True)
    )
    return {"id": client.id, "name": client.name, "phone_number": client.phone_number, "city": client.city, "address": client.address, "is_active": client.is_active}

def update_client(client_id, data):
    try:
        client = Client.objects.get(id=client_id)
        client.name = data.get('name', client.name)
        client.phone_number = data.get('phone_number', client.phone_number)
        client.city = data.get('city', client.city)
        client.address = data.get('address', client.address)
        client.is_active = data.get('is_active', client.is_active)
        client.save()
        return {"id": client.id, "name": client.name, "phone_number": client.phone_number, "city": client.city, "address": client.address, "is_active": client.is_active}
    except ObjectDoesNotExist:
        return None

def delete_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        client.delete()
        return True
    except ObjectDoesNotExist:
        return False
