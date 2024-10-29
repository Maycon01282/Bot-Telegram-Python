from django.core.exceptions import ObjectDoesNotExist
from api.models.user_model import User

class UserService:
    def list_users(self):
        users = User.objects.all()
        return [{"id": user.id, "name": user.name, "email": user.email} for user in users]

    def get_user_by_id(self, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            return {"id": user.id, "name": user.name, "email": user.email}
        except ObjectDoesNotExist:
            return None

    def get_user_by_email(self, email: str):
        try:
            user = User.objects.get(email=email)
            return {"id": user.id, "name": user.name, "email": user.email}
        except ObjectDoesNotExist:
            return None

    def create_user(self, data):
        user = User.objects.create(
            name=data['name'],
            email=data['email']
        )
        return {"id": user.id, "name": user.name, "email": user.email}

    def update_user(self, user_id: int, data):
        try:
            user = User.objects.get(id=user_id)
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.save()
            return {"id": user.id, "name": user.name, "email": user.email}
        except ObjectDoesNotExist:
            return None

    def delete_user(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False
