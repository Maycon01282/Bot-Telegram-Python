from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        except ObjectDoesNotExist:
            return None

    def get_user_by_id(self, user_id: int):
        """
        Retorna um usuário pelo ID ou None se não for encontrado.
        """
        try:
            user = User.objects.get(id=user_id)
            return {"id": user.id, "name": user.name, "email": user.email}
        except User.DoesNotExist:
            return None

    def list_users(self, page: int = 1, page_size: int = 10) -> dict:
        users = User.objects.all()
        paginator = Paginator(users, page_size)
        
        try:
            users_page = paginator.page(page)
        except PageNotAnInteger:
            users_page = paginator.page(1)
        except EmptyPage:
            users_page = paginator.page(paginator.num_pages)
        
        return {
            "users": [{"id": user.id, "name": user.name, "email": user.email} for user in users_page],
            "total_pages": paginator.num_pages,
            "current_page": users_page.number,
            "has_next": users_page.has_next(),
            "has_previous": users_page.has_previous()
        }
