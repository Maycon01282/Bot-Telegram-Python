from django.core.exceptions import ObjectDoesNotExist
from api.models.user_model import User

class UserService:
    def create_user(self, data):
        user = User.objects.create_user(
            email=data['email'],
            name=data['name'],
            password=data['password']
        )
        return {"id": user.id, "name": user.name, "email": user.email}

    def update_user(self, user_id: int, data):
        try:
            user = User.objects.get(id=user_id)
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.set_password(data['password'])
            user.save()
            return {"id": user.id, "name": user.name, "email": user.email}
        except User.DoesNotExist:
            raise User.DoesNotExist(f"User with id {user_id} does not exist")

    def delete_user(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def get_user_by_id(self, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            return {"id": user.id, "name": user.name, "email": user.email}
        except ObjectDoesNotExist:
            return None

    def list_users(self):
        users = User.objects.all()
        return [{"id": user.id, "name": user.name, "email": user.email} for user in users]